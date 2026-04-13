package strategy

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Strategy struct {
	ID          uuid.UUID      `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID      uuid.UUID      `gorm:"type:uuid;not null;index" json:"user_id"`
	Name        string         `gorm:"size:100;not null" json:"name"`
	Description string         `gorm:"type:text" json:"description"`
	Type        string         `gorm:"size:50;not null" json:"type"`
	Status      string         `gorm:"size:20;default:draft" json:"status"`
	Config      string         `gorm:"type:jsonb;not null" json:"config"`
	RiskConfig  string         `gorm:"type:jsonb" json:"risk_config"`
	Performance string         `gorm:"type:jsonb" json:"performance"`
	CreatedAt   time.Time      `json:"created_at"`
	UpdatedAt   time.Time      `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `gorm:"index" json:"-"`
}

func (Strategy) TableName() string {
	return "strategies"
}