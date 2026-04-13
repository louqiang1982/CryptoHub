package settings

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
	settings := r.Group("/settings")
	settings.GET("/", h.GetSettings)
	settings.PUT("/", h.UpdateSettings)
	settings.GET("/api-keys", h.ListAPIKeys)
	settings.POST("/api-keys", h.CreateAPIKey)
	settings.DELETE("/api-keys/:id", h.DeleteAPIKey)
}

func (h *Handler) GetSettings(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	settings, err := h.service.GetUserSettings(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to get settings")
		return
	}

	response.Success(c, settings)
}

func (h *Handler) UpdateSettings(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	var req map[string]interface{}
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	err := h.service.UpdateUserSettings(c.Request.Context(), userID.(string), req)
	if err != nil {
		response.InternalError(c, "Failed to update settings")
		return
	}

	response.Success(c, nil)
}

func (h *Handler) ListAPIKeys(c *gin.Context) {
	response.Success(c, gin.H{"api_keys": []gin.H{}})
}

func (h *Handler) CreateAPIKey(c *gin.Context) {
	response.Success(c, gin.H{"message": "API key created"})
}

func (h *Handler) DeleteAPIKey(c *gin.Context) {
	response.Success(c, nil)
}