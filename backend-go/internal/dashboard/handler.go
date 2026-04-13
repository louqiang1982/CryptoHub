package dashboard

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
	dashboard := r.Group("/dashboard")
	dashboard.GET("/stats", h.GetDashboardStats)
	dashboard.GET("/portfolio", h.GetPortfolioOverview)
	dashboard.GET("/recent-activity", h.GetRecentActivity)
}

func (h *Handler) GetDashboardStats(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	stats, err := h.service.GetDashboardStats(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get dashboard stats")
		return
	}

	response.Success(c, stats)
}

func (h *Handler) GetPortfolioOverview(c *gin.Context) {
	_, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	// Mock response for now
	response.Success(c, gin.H{
		"total_value": "10000.00",
		"assets":      []gin.H{},
	})
}

func (h *Handler) GetRecentActivity(c *gin.Context) {
	_, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	// Mock response for now
	response.Success(c, gin.H{
		"activities": []gin.H{},
	})
}