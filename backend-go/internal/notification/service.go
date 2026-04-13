package notification

import (
	"context"
	"encoding/json"
	"strconv"
	"time"

	"gorm.io/gorm"
	"github.com/google/uuid"
	"github.com/lib/pq"
)

type Service struct {
	db *gorm.DB
}

type Notification struct {
	ID        uuid.UUID      `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID    uuid.UUID      `gorm:"type:uuid;not null;index" json:"user_id"`
	Type      string         `gorm:"size:50;not null" json:"type"`
	Title     string         `gorm:"size:255;not null" json:"title"`
	Message   string         `gorm:"type:text;not null" json:"message"`
	Data      string         `gorm:"type:jsonb" json:"data,omitempty"`
	Status    string         `gorm:"size:20;default:unread" json:"status"`
	Priority  string         `gorm:"size:20;default:normal" json:"priority"`
	Channels  pq.StringArray `gorm:"type:text[];default:'{app}'" json:"channels"`
	SentAt    *time.Time     `json:"sent_at,omitempty"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
}

func NewService(db *gorm.DB) *Service {
	return &Service{db: db}
}

func (s *Service) ListNotifications(ctx context.Context, userID, status, limitStr string) ([]*Notification, error) {
	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 20
	}

	query := s.db.WithContext(ctx).Where("user_id = ?", userID)
	
	if status != "" {
		query = query.Where("status = ?", status)
	}

	var notifications []*Notification
	err = query.Order("created_at DESC").Limit(limit).Find(&notifications).Error
	return notifications, err
}

func (s *Service) GetNotification(ctx context.Context, userID, notificationID string) (*Notification, error) {
	var notification Notification
	err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", notificationID, userID).First(&notification).Error
	return &notification, err
}

func (s *Service) MarkAsRead(ctx context.Context, userID, notificationID string) error {
	return s.db.WithContext(ctx).Model(&Notification{}).
		Where("id = ? AND user_id = ?", notificationID, userID).
		Update("status", "read").Error
}

func (s *Service) MarkAllAsRead(ctx context.Context, userID string) error {
	return s.db.WithContext(ctx).Model(&Notification{}).
		Where("user_id = ? AND status = ?", userID, "unread").
		Update("status", "read").Error
}

func (s *Service) DeleteNotification(ctx context.Context, userID, notificationID string) error {
	return s.db.WithContext(ctx).Where("id = ? AND user_id = ?", notificationID, userID).Delete(&Notification{}).Error
}

func (s *Service) CreateNotification(ctx context.Context, userID, notificationType, title, message string, data interface{}, priority string, channels []string) error {
	var dataJSON string
	if data != nil {
		dataBytes, _ := json.Marshal(data)
		dataJSON = string(dataBytes)
	}

	notification := &Notification{
		UserID:   uuid.MustParse(userID),
		Type:     notificationType,
		Title:    title,
		Message:  message,
		Data:     dataJSON,
		Priority: priority,
		Channels: channels,
	}

	return s.db.WithContext(ctx).Create(notification).Error
}

func (s *Service) ProcessNotificationTask(ctx context.Context, payload []byte) error {
	// Implementation for processing notification tasks from queue
	return nil
}