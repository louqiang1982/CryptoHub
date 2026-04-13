package depth

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct{ service *Service }

func NewHandler(s *Service) *Handler { return &Handler{s} }

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	d := r.Group("/market/depth")
	d.GET("/:symbol", h.GetDepth)
}

func (h *Handler) GetDepth(c *gin.Context) {
	response.Success(c, map[string]interface{}{"bids": []interface{}{}, "asks": []interface{}{}})
}
