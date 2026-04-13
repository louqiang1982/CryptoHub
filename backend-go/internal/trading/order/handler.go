package order

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"github.com/louqiang1982/CryptoHub/backend-go/pkg/response"
)

type Handler struct {
	service *Service
}

func NewHandler(service *Service) *Handler {
	return &Handler{service: service}
}

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	orders := r.Group("/trading/orders")
	orders.POST("/", h.CreateOrder)
	orders.GET("/", h.ListOrders)
	orders.GET("/:id", h.GetOrder)
	orders.DELETE("/:id", h.CancelOrder)
	orders.PUT("/:id", h.UpdateOrder)
	orders.GET("/active", h.GetActiveOrders)
	orders.GET("/history", h.GetOrderHistory)
}

type CreateOrderRequest struct {
	Exchange    string          `json:"exchange" binding:"required"`
	Symbol      string          `json:"symbol" binding:"required"`
	Side        string          `json:"side" binding:"required,oneof=BUY SELL"`
	Type        string          `json:"type" binding:"required,oneof=MARKET LIMIT STOP_LOSS STOP_LOSS_LIMIT"`
	Quantity    decimal.Decimal `json:"quantity" binding:"required"`
	Price       decimal.Decimal `json:"price"`
	StopPrice   decimal.Decimal `json:"stop_price"`
	TimeInForce string          `json:"time_in_force"`
	StrategyID  string          `json:"strategy_id"`
}

func (h *Handler) CreateOrder(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	var req CreateOrderRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	order := &Order{
		UserID:      uuid.MustParse(userID.(string)),
		Exchange:    req.Exchange,
		Symbol:      req.Symbol,
		Side:        req.Side,
		Type:        req.Type,
		Status:      "NEW",
		TimeInForce: req.TimeInForce,
		Quantity:    req.Quantity,
		Price:       req.Price,
		StopPrice:   req.StopPrice,
	}

	if req.StrategyID != "" {
		strategyID, err := uuid.Parse(req.StrategyID)
		if err != nil {
			response.BadRequest(c, "Invalid strategy ID")
			return
		}
		order.StrategyID = strategyID
	}

	result, err := h.service.CreateOrder(c.Request.Context(), order)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, result)
}

func (h *Handler) ListOrders(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	page := c.DefaultQuery("page", "1")
	limit := c.DefaultQuery("limit", "20")
	symbol := c.Query("symbol")
	status := c.Query("status")
	exchange := c.Query("exchange")

	orders, total, err := h.service.ListOrders(c.Request.Context(), userID.(string), page, limit, symbol, status, exchange)
	if err != nil {
		response.InternalError(c, "Failed to list orders")
		return
	}

	response.Success(c, gin.H{
		"orders": orders,
		"total":  total,
	})
}

func (h *Handler) GetOrder(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	orderID := c.Param("id")
	if _, err := uuid.Parse(orderID); err != nil {
		response.BadRequest(c, "Invalid order ID")
		return
	}

	order, err := h.service.GetOrder(c.Request.Context(), userID.(string), orderID)
	if err != nil {
		response.NotFound(c, "Order not found")
		return
	}

	response.Success(c, order)
}

func (h *Handler) CancelOrder(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	orderID := c.Param("id")
	if _, err := uuid.Parse(orderID); err != nil {
		response.BadRequest(c, "Invalid order ID")
		return
	}

	err := h.service.CancelOrder(c.Request.Context(), userID.(string), orderID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	c.Status(http.StatusNoContent)
}

func (h *Handler) UpdateOrder(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	orderID := c.Param("id")
	if _, err := uuid.Parse(orderID); err != nil {
		response.BadRequest(c, "Invalid order ID")
		return
	}

	var req struct {
		Status string `json:"status"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	err := h.service.UpdateOrderStatus(c.Request.Context(), userID.(string), orderID, req.Status)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) GetActiveOrders(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	orders, err := h.service.GetActiveOrders(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get active orders")
		return
	}

	response.Success(c, orders)
}

func (h *Handler) GetOrderHistory(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	page := c.DefaultQuery("page", "1")
	limit := c.DefaultQuery("limit", "50")

	orders, total, err := h.service.GetOrderHistory(c.Request.Context(), userID.(string), page, limit)
	if err != nil {
		response.InternalError(c, "Failed to get order history")
		return
	}

	response.Success(c, gin.H{
		"orders": orders,
		"total":  total,
	})
}