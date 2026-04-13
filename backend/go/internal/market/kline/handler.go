package kline

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct{ service *Service }

func NewHandler(s *Service) *Handler { return &Handler{s} }

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	klines := r.Group("/market/klines")
	klines.GET("/", h.GetKlines)
}

func (h *Handler) GetKlines(c *gin.Context) { response.Success(c, []interface{}{}) }
