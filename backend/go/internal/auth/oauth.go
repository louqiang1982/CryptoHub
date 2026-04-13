package auth

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend/go/internal/user"
)

// OAuthRequest represents an OAuth login/registration request from the frontend.
type OAuthRequest struct {
	Provider   string `json:"provider" binding:"required"`
	ProviderID string `json:"provider_id" binding:"required"`
	Email      string `json:"email"`
	Name       string `json:"name"`
	Avatar     string `json:"avatar"`
}

// OAuthLogin handles login or registration via an OAuth provider.
// It looks up the user by provider+provider_id or email, creates a new user
// if not found, and returns a JWT token pair.
func (s *Service) OAuthLogin(ctx context.Context, req *OAuthRequest) (*TokenPair, error) {
	var u user.User

	// Try to find user by email first
	if req.Email != "" {
		err := s.db.WithContext(ctx).Where("email = ?", req.Email).First(&u).Error
		if err != nil && !errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, err
		}
		if err == nil {
			// Existing user found by email — issue tokens
			return s.generateTokens(ctx, u.ID.String())
		}
	}

	// No existing user — create a new one
	username := req.Name
	if username == "" {
		pid := req.ProviderID
		if len(pid) > 8 {
			pid = pid[:8]
		}
		username = req.Provider + "_" + pid
	}

	// Ensure unique username
	var existing user.User
	if err := s.db.WithContext(ctx).Where("username = ?", username).First(&existing).Error; err == nil {
		username = username + "_" + uuid.New().String()[:8]
	}

	u = user.User{
		ID:       uuid.New(),
		Email:    req.Email,
		Username: username,
		Password: "", // OAuth users have no password
		Avatar:   req.Avatar,
		Role:     "user",
		Status:   "active",
		Plan:     "free",
	}

	if err := s.db.WithContext(ctx).Create(&u).Error; err != nil {
		return nil, err
	}

	return s.generateTokens(ctx, u.ID.String())
}
