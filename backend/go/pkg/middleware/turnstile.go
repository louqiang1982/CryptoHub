package middleware

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

const turnstileVerifyURL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

// TurnstileResponse represents the Cloudflare verification response.
type TurnstileResponse struct {
	Success     bool      `json:"success"`
	ChallengeTS time.Time `json:"challenge_ts"`
	Hostname    string    `json:"hostname"`
	ErrorCodes  []string  `json:"error-codes"`
}

// Turnstile returns a Gin middleware that validates Cloudflare Turnstile tokens.
// The client must include the token in the "cf-turnstile-response" header or in the
// JSON body field "turnstile_token".
// If secretKey is empty the middleware is a no-op (useful for development).
func Turnstile(secretKey string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Skip verification if no secret key is configured (dev mode)
		if secretKey == "" {
			c.Next()
			return
		}

		// Extract token from header or body
		token := c.GetHeader("cf-turnstile-response")
		if token == "" {
			// Try to peek at JSON body for the token
			type body struct {
				TurnstileToken string `json:"turnstile_token"`
			}
			var b body
			if err := c.ShouldBindJSON(&b); err == nil && b.TurnstileToken != "" {
				token = b.TurnstileToken
			}
		}

		if token == "" {
			response.BadRequest(c, "Missing Turnstile token")
			c.Abort()
			return
		}

		// Verify with Cloudflare
		payload := "secret=" + secretKey + "&response=" + token + "&remoteip=" + c.ClientIP()
		resp, err := http.Post(turnstileVerifyURL, "application/x-www-form-urlencoded", strings.NewReader(payload))
		if err != nil {
			response.InternalError(c, "Turnstile verification failed")
			c.Abort()
			return
		}
		defer resp.Body.Close()

		var result TurnstileResponse
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			response.InternalError(c, "Failed to parse Turnstile response")
			c.Abort()
			return
		}

		if !result.Success {
			response.Forbidden(c, "Turnstile verification failed")
			c.Abort()
			return
		}

		c.Next()
	}
}
