package user

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type User struct {
	ID        uuid.UUID      `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	Email     string         `gorm:"uniqueIndex;not null;size:255" json:"email"`
	Username  string         `gorm:"uniqueIndex;not null;size:100" json:"username"`
	Password  string         `gorm:"not null" json:"-"`
	Avatar    string         `gorm:"size:500" json:"avatar"`
	Role      string         `gorm:"default:user;size:20" json:"role"`
	Status    string         `gorm:"default:active;size:20" json:"status"`
	Plan      string         `gorm:"default:free;size:20" json:"plan"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

type UserProfile struct {
	FirstName   string `json:"first_name"`
	LastName    string `json:"last_name"`
	Phone       string `json:"phone"`
	Country     string `json:"country"`
	Timezone    string `json:"timezone"`
	Language    string `json:"language"`
	TwoFAEnabled bool  `json:"two_fa_enabled"`
}

type UserPreferences struct {
	Theme                string `json:"theme"`
	NotificationEmail    bool   `json:"notification_email"`
	NotificationPush     bool   `json:"notification_push"`
	NotificationTelegram bool   `json:"notification_telegram"`
	TradingMode          string `json:"trading_mode"`
	RiskLevel            string `json:"risk_level"`
}