package portfolio

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend-go/pkg/response"
)

type Handler struct{ service *Service }

func NewHandler(s *Service) *Handler { return &Handler{s} }

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	portfolios := r.Group("/trading/portfolios")
	portfolios.GET("/", h.ListPortfolios)
}

func (h *Handler) ListPortfolios(c *gin.Context) { response.Success(c, []interface{}{}) }
