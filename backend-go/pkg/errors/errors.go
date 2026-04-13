package errors

import (
	"fmt"
	"net/http"
)

type APIError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Type    string `json:"type"`
}

func (e *APIError) Error() string {
	return fmt.Sprintf("API Error %d: %s", e.Code, e.Message)
}

var (
	ErrNotFound = &APIError{
		Code:    http.StatusNotFound,
		Message: "Resource not found",
		Type:    "NOT_FOUND",
	}

	ErrUnauthorized = &APIError{
		Code:    http.StatusUnauthorized,
		Message: "Unauthorized access",
		Type:    "UNAUTHORIZED",
	}

	ErrForbidden = &APIError{
		Code:    http.StatusForbidden,
		Message: "Access forbidden",
		Type:    "FORBIDDEN",
	}

	ErrBadRequest = &APIError{
		Code:    http.StatusBadRequest,
		Message: "Bad request",
		Type:    "BAD_REQUEST",
	}

	ErrInternal = &APIError{
		Code:    http.StatusInternalServerError,
		Message: "Internal server error",
		Type:    "INTERNAL_ERROR",
	}

	ErrValidation = &APIError{
		Code:    http.StatusUnprocessableEntity,
		Message: "Validation failed",
		Type:    "VALIDATION_ERROR",
	}

	ErrConflict = &APIError{
		Code:    http.StatusConflict,
		Message: "Resource conflict",
		Type:    "CONFLICT",
	}

	ErrTooManyRequests = &APIError{
		Code:    http.StatusTooManyRequests,
		Message: "Too many requests",
		Type:    "RATE_LIMIT",
	}
)

func NewAPIError(code int, message, errorType string) *APIError {
	return &APIError{
		Code:    code,
		Message: message,
		Type:    errorType,
	}
}

func NewNotFoundError(message string) *APIError {
	return &APIError{
		Code:    http.StatusNotFound,
		Message: message,
		Type:    "NOT_FOUND",
	}
}

func NewBadRequestError(message string) *APIError {
	return &APIError{
		Code:    http.StatusBadRequest,
		Message: message,
		Type:    "BAD_REQUEST",
	}
}

func NewInternalError(message string) *APIError {
	return &APIError{
		Code:    http.StatusInternalServerError,
		Message: message,
		Type:    "INTERNAL_ERROR",
	}
}