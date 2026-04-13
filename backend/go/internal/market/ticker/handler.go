package ticker

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct{ service *Service }

func NewHandler(s *Service) *Handler { return &Handler{s} }

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	t := r.Group("/market/ticker")
	t.GET("/:symbol", h.GetTicker)
}

func (h *Handler) GetTicker(c *gin.Context) {
	response.Success(c, map[string]interface{}{"symbol": c.Param("symbol"), "price": "0"})
}
