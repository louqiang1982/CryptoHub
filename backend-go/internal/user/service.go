package user

import (
	"context"
	"strconv"
)

type Service struct {
	repo *Repository
}

func NewService(repo *Repository) *Service {
	return &Service{repo: repo}
}

func (s *Service) GetByID(ctx context.Context, id string) (*User, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *Service) GetByEmail(ctx context.Context, email string) (*User, error) {
	return s.repo.GetByEmail(ctx, email)
}

func (s *Service) GetByUsername(ctx context.Context, username string) (*User, error) {
	return s.repo.GetByUsername(ctx, username)
}

func (s *Service) Create(ctx context.Context, user *User) error {
	return s.repo.Create(ctx, user)
}

func (s *Service) UpdateProfile(ctx context.Context, id, username, avatar string) (*User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	if username != "" {
		user.Username = username
	}
	if avatar != "" {
		user.Avatar = avatar
	}

	err = s.repo.Update(ctx, user)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (s *Service) UpdateStatus(ctx context.Context, id, status string) error {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}

	user.Status = status
	return s.repo.Update(ctx, user)
}

func (s *Service) Delete(ctx context.Context, id string) error {
	return s.repo.Delete(ctx, id)
}

func (s *Service) List(ctx context.Context, pageStr, limitStr, search string) ([]*User, int64, error) {
	page, err := strconv.Atoi(pageStr)
	if err != nil {
		page = 1
	}

	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 10
	}

	offset := (page - 1) * limit

	users, err := s.repo.List(ctx, limit, offset, search)
	if err != nil {
		return nil, 0, err
	}

	total, err := s.repo.Count(ctx, search)
	if err != nil {
		return nil, 0, err
	}

	return users, total, nil
}