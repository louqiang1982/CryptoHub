package position

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend-go/pkg/response"
)

type Handler struct {
	service *Service
}

func NewHandler(service *Service) *Handler {
	return &Handler{service: service}
}

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	positions := r.Group("/trading/positions")
	positions.GET("/", h.ListPositions)
	positions.GET("/:id", h.GetPosition)
	positions.PUT("/:id/close", h.ClosePosition)
	positions.GET("/open", h.GetOpenPositions)
	positions.GET("/summary", h.GetPositionSummary)
}

func (h *Handler) ListPositions(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	page := c.DefaultQuery("page", "1")
	limit := c.DefaultQuery("limit", "20")
	symbol := c.Query("symbol")
	status := c.Query("status")

	positions, total, err := h.service.ListPositions(c.Request.Context(), userID.(string), page, limit, symbol, status)
	if err != nil {
		response.InternalError(c, "Failed to list positions")
		return
	}

	response.Success(c, gin.H{
		"positions": positions,
		"total":     total,
	})
}

func (h *Handler) GetPosition(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	positionID := c.Param("id")
	position, err := h.service.GetPosition(c.Request.Context(), userID.(string), positionID)
	if err != nil {
		response.NotFound(c, "Position not found")
		return
	}

	response.Success(c, position)
}

func (h *Handler) ClosePosition(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	positionID := c.Param("id")
	err := h.service.ClosePosition(c.Request.Context(), userID.(string), positionID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) GetOpenPositions(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	positions, err := h.service.GetOpenPositions(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get open positions")
		return
	}

	response.Success(c, positions)
}

func (h *Handler) GetPositionSummary(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	summary, err := h.service.GetPositionSummary(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get position summary")
		return
	}

	response.Success(c, summary)
}