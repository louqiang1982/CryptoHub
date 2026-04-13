package portfolio

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct {
	service *Service
}

func NewHandler(s *Service) *Handler { return &Handler{service: s} }

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	portfolios := r.Group("/trading/portfolios")
	portfolios.GET("", h.ListPortfolios)
	portfolios.GET("/summary", h.GetSummary)
	portfolios.GET("/:id", h.GetPortfolio)
	portfolios.POST("", h.CreatePortfolio)
	portfolios.PUT("/:id", h.UpdatePortfolio)
	portfolios.DELETE("/:id", h.DeletePortfolio)
}

func (h *Handler) ListPortfolios(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}
	portfolios, err := h.service.ListPortfolios(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to list portfolios")
		return
	}
	response.Success(c, portfolios)
}

func (h *Handler) GetPortfolio(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}
	id := c.Param("id")

	p, err := h.service.GetPortfolio(c.Request.Context(), userID.(string), id)
	if err != nil {
		response.NotFound(c, err.Error())
		return
	}
	response.Success(c, p)
}

func (h *Handler) CreatePortfolio(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	var req CreateRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	p, err := h.service.CreatePortfolio(c.Request.Context(), userID.(string), &req)
	if err != nil {
		response.InternalError(c, err.Error())
		return
	}
	response.Success(c, p)
}

func (h *Handler) UpdatePortfolio(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}
	id := c.Param("id")

	var req UpdateRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	p, err := h.service.UpdatePortfolio(c.Request.Context(), userID.(string), id, &req)
	if err != nil {
		response.NotFound(c, err.Error())
		return
	}
	response.Success(c, p)
}

func (h *Handler) DeletePortfolio(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}
	id := c.Param("id")

	if err := h.service.DeletePortfolio(c.Request.Context(), userID.(string), id); err != nil {
		response.NotFound(c, err.Error())
		return
	}
	response.Success(c, nil)
}

func (h *Handler) GetSummary(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	summary, err := h.service.GetSummary(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get portfolio summary")
		return
	}
	response.Success(c, summary)
}
