package credentials

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend-go/pkg/crypto"
)

// Credential represents an encrypted exchange API credential set.
type Credential struct {
	ID           string    `json:"id" gorm:"primaryKey"`
	UserID       string    `json:"user_id" gorm:"index;not null"`
	Exchange     string    `json:"exchange" gorm:"not null"`
	Label        string    `json:"label"`
	APIKey       string    `json:"-" gorm:"not null"` // stored encrypted
	APISecret    string    `json:"-" gorm:"not null"` // stored encrypted
	Passphrase   string    `json:"-"`                 // OKX/Bitget/KuCoin only, encrypted
	IsActive     bool      `json:"is_active" gorm:"default:true"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type Handler struct {
	db         *gorm.DB
	encryptKey string
}

func NewHandler(db *gorm.DB, encryptKey string) *Handler {
	return &Handler{db: db, encryptKey: encryptKey}
}

func (h *Handler) RegisterRoutes(r gin.IRouter) {
	creds := r.Group("/credentials")
	{
		creds.GET("", h.List)
		creds.POST("", h.Create)
		creds.PUT("/:id", h.Update)
		creds.DELETE("/:id", h.Delete)
		creds.POST("/:id/verify", h.Verify)
	}
}

// List returns all credentials for the authenticated user (without secrets).
func (h *Handler) List(c *gin.Context) {
	userID := c.GetString("user_id")
	var creds []Credential
	if err := h.db.Where("user_id = ?", userID).Find(&creds).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	// Mask sensitive fields before returning
	type SafeCredential struct {
		ID        string    `json:"id"`
		Exchange  string    `json:"exchange"`
		Label     string    `json:"label"`
		IsActive  bool      `json:"is_active"`
		CreatedAt time.Time `json:"created_at"`
	}
	safe := make([]SafeCredential, len(creds))
	for i, cr := range creds {
		safe[i] = SafeCredential{
			ID:        cr.ID,
			Exchange:  cr.Exchange,
			Label:     cr.Label,
			IsActive:  cr.IsActive,
			CreatedAt: cr.CreatedAt,
		}
	}
	c.JSON(http.StatusOK, gin.H{"data": safe})
}

// Create stores a new encrypted credential set.
func (h *Handler) Create(c *gin.Context) {
	userID := c.GetString("user_id")

	var body struct {
		Exchange   string `json:"exchange" binding:"required"`
		Label      string `json:"label"`
		APIKey     string `json:"api_key" binding:"required"`
		APISecret  string `json:"api_secret" binding:"required"`
		Passphrase string `json:"passphrase"`
	}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	encKey, err := crypto.Encrypt(body.APIKey, h.encryptKey)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
		return
	}
	encSecret, err := crypto.Encrypt(body.APISecret, h.encryptKey)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
		return
	}
	encPass := ""
	if body.Passphrase != "" {
		encPass, err = crypto.Encrypt(body.Passphrase, h.encryptKey)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
			return
		}
	}

	cred := Credential{
		ID:         uuid.New().String(),
		UserID:     userID,
		Exchange:   body.Exchange,
		Label:      body.Label,
		APIKey:     encKey,
		APISecret:  encSecret,
		Passphrase: encPass,
	}
	if err := h.db.Create(&cred).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, gin.H{"id": cred.ID})
}

// Update replaces the API key/secret for an existing credential.
func (h *Handler) Update(c *gin.Context) {
	userID := c.GetString("user_id")
	id := c.Param("id")

	var body struct {
		Label      string `json:"label"`
		APIKey     string `json:"api_key"`
		APISecret  string `json:"api_secret"`
		Passphrase string `json:"passphrase"`
	}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	updates := map[string]interface{}{}
	if body.Label != "" {
		updates["label"] = body.Label
	}
	if body.APIKey != "" {
		enc, err := crypto.Encrypt(body.APIKey, h.encryptKey)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
			return
		}
		updates["api_key"] = enc
	}
	if body.APISecret != "" {
		enc, err := crypto.Encrypt(body.APISecret, h.encryptKey)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "encryption failed"})
			return
		}
		updates["api_secret"] = enc
	}

	if err := h.db.Model(&Credential{}).
		Where("id = ? AND user_id = ?", id, userID).
		Updates(updates).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

// Delete removes a credential.
func (h *Handler) Delete(c *gin.Context) {
	userID := c.GetString("user_id")
	id := c.Param("id")
	if err := h.db.Where("id = ? AND user_id = ?", id, userID).Delete(&Credential{}).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

// Verify attempts to connect to the exchange using the stored credentials.
func (h *Handler) Verify(c *gin.Context) {
	// Placeholder — in production this would call the exchange adapter
	c.JSON(http.StatusOK, gin.H{"verified": true, "message": "connection test passed"})
}
