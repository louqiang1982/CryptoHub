package admin

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
	admin := r
	admin.GET("/stats", h.GetSystemStats)
	admin.GET("/users", h.ListUsers)
	admin.GET("/audit-logs", h.GetAuditLogs)
}

func (h *Handler) GetSystemStats(c *gin.Context) {
	stats, err := h.service.GetSystemStats(c.Request.Context())
	if err != nil {
		response.InternalError(c, "Failed to get system stats")
		return
	}

	response.Success(c, stats)
}

func (h *Handler) ListUsers(c *gin.Context) {
	response.Success(c, gin.H{"users": []gin.H{}})
}

func (h *Handler) GetAuditLogs(c *gin.Context) {
	response.Success(c, gin.H{"logs": []gin.H{}})
}