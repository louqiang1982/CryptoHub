package user

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct {
	service *Service
}

func NewHandler(service *Service) *Handler {
	return &Handler{service: service}
}

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	users := r.Group("/users")
	users.GET("/profile", h.GetProfile)
	users.PUT("/profile", h.UpdateProfile)
	users.GET("/", h.ListUsers)
	users.GET("/:id", h.GetUser)
	users.PUT("/:id", h.UpdateUser)
	users.DELETE("/:id", h.DeleteUser)
	users.PUT("/:id/status", h.UpdateUserStatus)
}

type UpdateProfileRequest struct {
	Username string `json:"username"`
	Avatar   string `json:"avatar"`
}

func (h *Handler) GetProfile(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	user, err := h.service.GetByID(c.Request.Context(), userID.(string))
	if err != nil {
		response.NotFound(c, "User not found")
		return
	}

	response.Success(c, user)
}

func (h *Handler) UpdateProfile(c *gin.Context) {
	userID, exists := c.Get("user_id")
	if !exists {
		response.Unauthorized(c, "User not authenticated")
		return
	}

	var req UpdateProfileRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	user, err := h.service.UpdateProfile(c.Request.Context(), userID.(string), req.Username, req.Avatar)
	if err != nil {
		response.InternalError(c, "Failed to update profile")
		return
	}

	response.Success(c, user)
}

func (h *Handler) ListUsers(c *gin.Context) {
	// Admin only
	role, exists := c.Get("user_role")
	if !exists || role != "admin" {
		response.Forbidden(c, "Access denied")
		return
	}

	page := c.DefaultQuery("page", "1")
	limit := c.DefaultQuery("limit", "10")
	search := c.Query("search")

	users, total, err := h.service.List(c.Request.Context(), page, limit, search)
	if err != nil {
		response.InternalError(c, "Failed to list users")
		return
	}

	response.Success(c, gin.H{
		"users": users,
		"total": total,
	})
}

func (h *Handler) GetUser(c *gin.Context) {
	id := c.Param("id")
	if _, err := uuid.Parse(id); err != nil {
		response.BadRequest(c, "Invalid user ID")
		return
	}

	user, err := h.service.GetByID(c.Request.Context(), id)
	if err != nil {
		response.NotFound(c, "User not found")
		return
	}

	response.Success(c, user)
}

func (h *Handler) UpdateUser(c *gin.Context) {
	id := c.Param("id")
	if _, err := uuid.Parse(id); err != nil {
		response.BadRequest(c, "Invalid user ID")
		return
	}

	var req UpdateProfileRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	user, err := h.service.UpdateProfile(c.Request.Context(), id, req.Username, req.Avatar)
	if err != nil {
		response.InternalError(c, "Failed to update user")
		return
	}

	response.Success(c, user)
}

func (h *Handler) DeleteUser(c *gin.Context) {
	id := c.Param("id")
	if _, err := uuid.Parse(id); err != nil {
		response.BadRequest(c, "Invalid user ID")
		return
	}

	err := h.service.Delete(c.Request.Context(), id)
	if err != nil {
		response.InternalError(c, "Failed to delete user")
		return
	}

	c.Status(http.StatusNoContent)
}

func (h *Handler) UpdateUserStatus(c *gin.Context) {
	id := c.Param("id")
	if _, err := uuid.Parse(id); err != nil {
		response.BadRequest(c, "Invalid user ID")
		return
	}

	var req struct {
		Status string `json:"status" binding:"required"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	err := h.service.UpdateStatus(c.Request.Context(), id, req.Status)
	if err != nil {
		response.InternalError(c, "Failed to update user status")
		return
	}

	response.Success(c, nil)
}