package risk

import (
	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type Handler struct {
	engine *Engine
}

func NewHandler(engine *Engine) *Handler {
	return &Handler{engine: engine}
}

func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	risk := r.Group("/risk")
	risk.POST("/check", h.CheckOrderRisk)
	risk.GET("/portfolio/:id", h.GetPortfolioRisk)
	risk.GET("/config", h.GetRiskConfig)
	risk.PUT("/config", h.UpdateRiskConfig)
}

func (h *Handler) CheckOrderRisk(c *gin.Context) {
	var req OrderRiskRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	userID, _ := c.Get("user_id")
	req.UserID = userID.(string)

	result, err := h.engine.CheckOrderRisk(c.Request.Context(), &req)
	if err != nil {
		response.InternalError(c, "Risk check failed")
		return
	}
	response.Success(c, result)
}

func (h *Handler) GetPortfolioRisk(c *gin.Context) {
	userID, _ := c.Get("user_id")
	portfolioID := c.Param("id")

	report, err := h.engine.GetPortfolioRisk(c.Request.Context(), userID.(string), portfolioID)
	if err != nil {
		response.InternalError(c, "Failed to get portfolio risk")
		return
	}
	response.Success(c, report)
}

func (h *Handler) GetRiskConfig(c *gin.Context) {
	userID, _ := c.Get("user_id")
	config := h.engine.loadRiskConfig(c.Request.Context(), userID.(string))
	response.Success(c, config)
}

func (h *Handler) UpdateRiskConfig(c *gin.Context) {
	userID, _ := c.Get("user_id")

	var config RiskConfig
	if err := c.ShouldBindJSON(&config); err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	if err := h.engine.SaveRiskConfig(c.Request.Context(), userID.(string), &config); err != nil {
		response.InternalError(c, "Failed to save risk config")
		return
	}
	response.Success(c, config)
}
