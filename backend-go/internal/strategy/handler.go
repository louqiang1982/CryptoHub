package strategy

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
	strategies := r.Group("/strategies")
	strategies.GET("/", h.ListStrategies)
	strategies.POST("/", h.CreateStrategy)
	strategies.GET("/:id", h.GetStrategy)
	strategies.PUT("/:id", h.UpdateStrategy)
	strategies.DELETE("/:id", h.DeleteStrategy)
	strategies.POST("/:id/start", h.StartStrategy)
	strategies.POST("/:id/stop", h.StopStrategy)
	strategies.POST("/:id/pause", h.PauseStrategy)
}

func (h *Handler) ListStrategies(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategies, err := h.service.ListStrategies(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to list strategies")
		return
	}

	response.Success(c, strategies)
}

func (h *Handler) CreateStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	var req struct {
		Name        string `json:"name" binding:"required"`
		Description string `json:"description"`
		Type        string `json:"type" binding:"required"`
		Config      string `json:"config" binding:"required"`
		RiskConfig  string `json:"risk_config"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	strategy, err := h.service.CreateStrategy(c.Request.Context(), userID.(string), req.Name, req.Description, req.Type, req.Config, req.RiskConfig)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, strategy)
}

func (h *Handler) GetStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	strategy, err := h.service.GetStrategy(c.Request.Context(), userID.(string), strategyID)
	if err != nil {
		response.NotFound(c, "Strategy not found")
		return
	}

	response.Success(c, strategy)
}

func (h *Handler) UpdateStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	var req struct {
		Name        string `json:"name"`
		Description string `json:"description"`
		Config      string `json:"config"`
		RiskConfig  string `json:"risk_config"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	strategy, err := h.service.UpdateStrategy(c.Request.Context(), userID.(string), strategyID, req.Name, req.Description, req.Config, req.RiskConfig)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, strategy)
}

func (h *Handler) DeleteStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	err := h.service.DeleteStrategy(c.Request.Context(), userID.(string), strategyID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) StartStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	err := h.service.StartStrategy(c.Request.Context(), userID.(string), strategyID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) StopStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	err := h.service.StopStrategy(c.Request.Context(), userID.(string), strategyID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) PauseStrategy(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	strategyID := c.Param("id")
	err := h.service.PauseStrategy(c.Request.Context(), userID.(string), strategyID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}