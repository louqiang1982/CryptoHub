package dashboard

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
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
	dashboard.GET("/charts/drawdown", h.GetDrawdownData)
	dashboard.GET("/charts/profit-calendar", h.GetProfitCalendarData)
	dashboard.GET("/charts/strategy-distribution", h.GetStrategyDistribution)
	dashboard.GET("/charts/trading-hours", h.GetTradingHoursHeatmap)
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

func (h *Handler) GetDrawdownData(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	data, err := h.service.GetDrawdownCurve(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get drawdown data")
		return
	}

	response.Success(c, data)
}

func (h *Handler) GetProfitCalendarData(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	data, err := h.service.GetProfitCalendar(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get profit calendar data")
		return
	}

	response.Success(c, data)
}

func (h *Handler) GetStrategyDistribution(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	data, err := h.service.GetStrategyDistribution(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get strategy distribution")
		return
	}

	response.Success(c, data)
}

func (h *Handler) GetTradingHoursHeatmap(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	data, err := h.service.GetTradingHoursHeatmap(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get trading hours heatmap")
		return
	}

	response.Success(c, data)
}