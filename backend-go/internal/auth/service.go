package auth

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend-go/internal/user"
)

type Service struct {
	db  *gorm.DB
	rdb *redis.Client
}

type TokenPair struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    int64  `json:"expires_in"`
}

func NewService(db *gorm.DB, rdb *redis.Client) *Service {
	return &Service{
		db:  db,
		rdb: rdb,
	}
}

func (s *Service) Login(ctx context.Context, email, password string) (*TokenPair, error) {
	var u user.User
	if err := s.db.Where("email = ? AND status = ?", email, "active").First(&u).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, errors.New("invalid credentials")
		}
		return nil, err
	}

	if !checkPasswordHash(password, u.Password) {
		return nil, errors.New("invalid credentials")
	}

	return s.generateTokens(ctx, u.ID.String())
}

func (s *Service) Register(ctx context.Context, email, username, password string) (*TokenPair, error) {
	// Check if user already exists
	var existing user.User
	if err := s.db.Where("email = ? OR username = ?", email, username).First(&existing).Error; err == nil {
		return nil, errors.New("user already exists")
	}

	hashedPassword, err := hashPassword(password)
	if err != nil {
		return nil, err
	}

	u := user.User{
		ID:       uuid.New(),
		Email:    email,
		Username: username,
		Password: hashedPassword,
		Role:     "user",
		Status:   "active",
		Plan:     "free",
	}

	if err := s.db.Create(&u).Error; err != nil {
		return nil, err
	}

	return s.generateTokens(ctx, u.ID.String())
}

func (s *Service) RefreshToken(ctx context.Context, refreshToken string) (*TokenPair, error) {
	claims, err := ParseRefreshToken(refreshToken)
	if err != nil {
		return nil, err
	}

	// Check if refresh token is blacklisted
	exists, err := s.rdb.Exists(ctx, "blacklist:"+refreshToken).Result()
	if err != nil {
		return nil, err
	}
	if exists > 0 {
		return nil, errors.New("refresh token is invalid")
	}

	return s.generateTokens(ctx, claims.UserID)
}

func (s *Service) Logout(ctx context.Context, accessToken string) error {
	// Parse token to get expiration
	claims, err := ParseAccessToken(accessToken)
	if err != nil {
		return err
	}

	// Add token to blacklist with TTL
	ttl := time.Until(time.Unix(claims.ExpiresAt.Unix(), 0))
	if ttl > 0 {
		return s.rdb.SetEx(ctx, "blacklist:"+accessToken, "1", ttl).Err()
	}

	return nil
}

func (s *Service) GetProfile(ctx context.Context, userID string) (*user.User, error) {
	var u user.User
	if err := s.db.Where("id = ?", userID).First(&u).Error; err != nil {
		return nil, err
	}
	return &u, nil
}

func (s *Service) ValidateToken(ctx context.Context, token string) (*Claims, error) {
	// Check if token is blacklisted
	exists, err := s.rdb.Exists(ctx, "blacklist:"+token).Result()
	if err != nil {
		return nil, err
	}
	if exists > 0 {
		return nil, errors.New("token is blacklisted")
	}

	return ParseAccessToken(token)
}

func (s *Service) generateTokens(ctx context.Context, userID string) (*TokenPair, error) {
	accessToken, err := GenerateAccessToken(userID)
	if err != nil {
		return nil, err
	}

	refreshToken, err := GenerateRefreshToken(userID)
	if err != nil {
		return nil, err
	}

	return &TokenPair{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int64(24 * time.Hour.Seconds()), // 24 hours
	}, nil
}

func hashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(bytes), err
}

func checkPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}