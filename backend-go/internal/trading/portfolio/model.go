package portfolio

import (
	"time"
	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Portfolio struct {
	ID               uuid.UUID       `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID           uuid.UUID       `gorm:"type:uuid;not null;index" json:"user_id"`
	Name             string          `gorm:"size:100;not null" json:"name"`
	Type             string          `gorm:"size:20;default:live" json:"type"`
	Exchange         string          `gorm:"size:20;not null" json:"exchange"`
	BaseCurrency     string          `gorm:"size:10;default:USDT" json:"base_currency"`
	TotalValue       decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"total_value"`
	AvailableBalance decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"available_balance"`
	LockedBalance    decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"locked_balance"`
	UnrealizedPL     decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"unrealized_pl"`
	RealizedPL       decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"realized_pl"`
	CreatedAt        time.Time       `json:"created_at"`
	UpdatedAt        time.Time       `json:"updated_at"`
	DeletedAt        gorm.DeletedAt  `gorm:"index" json:"-"`
}

package portfolio

import ("github.com/gin-gonic/gin"; "github.com/louqiang1982/CryptoHub/backend-go/pkg/response")
type Handler struct { service *Service }
func NewHandler(s *Service) *Handler { return &Handler{s} }
func (h *Handler) RegisterRoutes(r *gin.RouterGroup) {
	portfolios := r.Group("/trading/portfolios")
	portfolios.GET("/", h.ListPortfolios)
}
func (h *Handler) ListPortfolios(c *gin.Context) { response.Success(c, []interface{}{}) }

package portfolio
import ("context"; "gorm.io/gorm")
type Service struct { db *gorm.DB }
func NewService(db *gorm.DB) *Service { return &Service{db} }