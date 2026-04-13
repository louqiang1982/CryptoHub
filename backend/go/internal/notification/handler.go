package notification

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
	notifications := r.Group("/notifications")
	notifications.GET("/", h.ListNotifications)
	notifications.GET("/:id", h.GetNotification)
	notifications.PUT("/:id/read", h.MarkAsRead)
	notifications.PUT("/read-all", h.MarkAllAsRead)
	notifications.DELETE("/:id", h.DeleteNotification)
}

func (h *Handler) ListNotifications(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	status := c.Query("status")
	limit := c.DefaultQuery("limit", "20")

	notifications, err := h.service.ListNotifications(c.Request.Context(), userID.(string), status, limit)
	if err != nil {
		response.InternalError(c, "Failed to list notifications")
		return
	}

	response.Success(c, notifications)
}

func (h *Handler) GetNotification(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	notificationID := c.Param("id")
	notification, err := h.service.GetNotification(c.Request.Context(), userID.(string), notificationID)
	if err != nil {
		response.NotFound(c, "Notification not found")
		return
	}

	response.Success(c, notification)
}

func (h *Handler) MarkAsRead(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	notificationID := c.Param("id")
	err := h.service.MarkAsRead(c.Request.Context(), userID.(string), notificationID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}

func (h *Handler) MarkAllAsRead(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	err := h.service.MarkAllAsRead(c.Request.Context(), userID.(string))
	if err != nil {
		response.InternalError(c, "Failed to mark all as read")
		return
	}

	response.Success(c, nil)
}

func (h *Handler) DeleteNotification(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	notificationID := c.Param("id")
	err := h.service.DeleteNotification(c.Request.Context(), userID.(string), notificationID)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, nil)
}