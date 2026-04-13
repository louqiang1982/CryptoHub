package community

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

// IndicatorPost represents a community-shared indicator/strategy post.
type IndicatorPost struct {
	ID          string    `json:"id" gorm:"primaryKey"`
	UserID      string    `json:"user_id" gorm:"index;not null"`
	Title       string    `json:"title" gorm:"not null"`
	Description string    `json:"description"`
	Code        string    `json:"code" gorm:"type:text"`
	Language    string    `json:"language" gorm:"default:'python'"`
	Tags        string    `json:"tags"`
	Likes       int       `json:"likes" gorm:"default:0"`
	Forks       int       `json:"forks" gorm:"default:0"`
	IsPublic    bool      `json:"is_public" gorm:"default:true"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// Comment on an indicator post.
type Comment struct {
	ID        string    `json:"id" gorm:"primaryKey"`
	PostID    string    `json:"post_id" gorm:"index;not null"`
	UserID    string    `json:"user_id" gorm:"index;not null"`
	Content   string    `json:"content" gorm:"type:text;not null"`
	CreatedAt time.Time `json:"created_at"`
}

type Handler struct {
	db *gorm.DB
}

func NewHandler(db *gorm.DB) *Handler {
	return &Handler{db: db}
}

func (h *Handler) RegisterRoutes(r gin.IRouter) {
	community := r.Group("/community")
	{
		community.GET("/posts", h.ListPosts)
		community.POST("/posts", h.CreatePost)
		community.GET("/posts/:id", h.GetPost)
		community.PUT("/posts/:id", h.UpdatePost)
		community.DELETE("/posts/:id", h.DeletePost)
		community.POST("/posts/:id/like", h.LikePost)
		community.POST("/posts/:id/fork", h.ForkPost)
		community.GET("/posts/:id/comments", h.ListComments)
		community.POST("/posts/:id/comments", h.AddComment)
	}
}

func (h *Handler) ListPosts(c *gin.Context) {
	var posts []IndicatorPost
	q := h.db.Where("is_public = ?", true).Order("created_at DESC")
	if tag := c.Query("tag"); tag != "" {
		q = q.Where("tags LIKE ?", "%"+tag+"%")
	}
	if err := q.Limit(50).Find(&posts).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"data": posts})
}

func (h *Handler) CreatePost(c *gin.Context) {
	userID := c.GetString("user_id")
	var body IndicatorPost
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	body.ID = uuid.New().String()
	body.UserID = userID
	if err := h.db.Create(&body).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, body)
}

func (h *Handler) GetPost(c *gin.Context) {
	var post IndicatorPost
	if err := h.db.First(&post, "id = ?", c.Param("id")).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "post not found"})
		return
	}
	c.JSON(http.StatusOK, post)
}

func (h *Handler) UpdatePost(c *gin.Context) {
	userID := c.GetString("user_id")
	var body map[string]interface{}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := h.db.Model(&IndicatorPost{}).
		Where("id = ? AND user_id = ?", c.Param("id"), userID).
		Updates(body).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *Handler) DeletePost(c *gin.Context) {
	userID := c.GetString("user_id")
	if err := h.db.Where("id = ? AND user_id = ?", c.Param("id"), userID).
		Delete(&IndicatorPost{}).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *Handler) LikePost(c *gin.Context) {
	h.db.Model(&IndicatorPost{}).Where("id = ?", c.Param("id")).
		UpdateColumn("likes", gorm.Expr("likes + 1"))
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *Handler) ForkPost(c *gin.Context) {
	userID := c.GetString("user_id")
	var src IndicatorPost
	if err := h.db.First(&src, "id = ?", c.Param("id")).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "post not found"})
		return
	}
	fork := IndicatorPost{
		ID:          uuid.New().String(),
		UserID:      userID,
		Title:       "Fork of " + src.Title,
		Description: src.Description,
		Code:        src.Code,
		Language:    src.Language,
		Tags:        src.Tags,
	}
	h.db.Create(&fork)
	h.db.Model(&IndicatorPost{}).Where("id = ?", src.ID).
		UpdateColumn("forks", gorm.Expr("forks + 1"))
	c.JSON(http.StatusCreated, fork)
}

func (h *Handler) ListComments(c *gin.Context) {
	var comments []Comment
	h.db.Where("post_id = ?", c.Param("id")).Order("created_at ASC").Find(&comments)
	c.JSON(http.StatusOK, gin.H{"data": comments})
}

func (h *Handler) AddComment(c *gin.Context) {
	userID := c.GetString("user_id")
	var body struct {
		Content string `json:"content" binding:"required"`
	}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	comment := Comment{
		ID:      uuid.New().String(),
		PostID:  c.Param("id"),
		UserID:  userID,
		Content: body.Content,
	}
	h.db.Create(&comment)
	c.JSON(http.StatusCreated, comment)
}
