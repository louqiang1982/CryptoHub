package billing

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
	billing := r.Group("/billing")
	billing.GET("/subscription", h.GetSubscription)
	billing.POST("/upgrade", h.UpgradeSubscription)
	billing.POST("/cancel", h.CancelSubscription)
}

func (h *Handler) GetSubscription(c *gin.Context) {
	userID, _ := c.Get("user_id")
	subscription, _ := h.service.GetSubscriptionInfo(c.Request.Context(), userID.(string))
	response.Success(c, subscription)
}

func (h *Handler) UpgradeSubscription(c *gin.Context) {
	userID, _ := c.Get("user_id")
	var req struct{ Plan string `json:"plan"` }
	c.ShouldBindJSON(&req)
	h.service.UpgradeSubscription(c.Request.Context(), userID.(string), req.Plan)
	response.Success(c, nil)
}

func (h *Handler) CancelSubscription(c *gin.Context) {
	userID, _ := c.Get("user_id")
	h.service.CancelSubscription(c.Request.Context(), userID.(string))
	response.Success(c, nil)
}