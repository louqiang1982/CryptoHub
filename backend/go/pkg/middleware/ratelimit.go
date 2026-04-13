package middleware

import (
	"context"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"github.com/louqiang1982/CryptoHub/backend/go/pkg/response"
)

type RateLimiter struct {
	rdb      *redis.Client
	rate     int
	window   time.Duration
	keyFunc  func(c *gin.Context) string
}

func RateLimit(rdb *redis.Client) gin.HandlerFunc {
	limiter := &RateLimiter{
		rdb:    rdb,
		rate:   100,        // 100 requests
		window: time.Minute, // per minute
		keyFunc: func(c *gin.Context) string {
			// Rate limit by IP address
			return "rate_limit:" + c.ClientIP()
		},
	}

	return func(c *gin.Context) {
		key := limiter.keyFunc(c)
		
		ctx := context.Background()
		
		// Get current count
		current, err := limiter.rdb.Get(ctx, key).Result()
		if err != nil && err != redis.Nil {
			// If Redis is down, allow the request
			c.Next()
			return
		}

		var count int
		if current != "" {
			count, _ = strconv.Atoi(current)
		}

		if count >= limiter.rate {
			response.BadRequest(c, "Rate limit exceeded")
			c.AbortWithStatus(http.StatusTooManyRequests)
			return
		}

		// Increment counter
		pipe := limiter.rdb.Pipeline()
		pipe.Incr(ctx, key)
		if count == 0 {
			pipe.Expire(ctx, key, limiter.window)
		}
		pipe.Exec(ctx)

		c.Next()
	}
}

func CustomRateLimit(rdb *redis.Client, rate int, window time.Duration, keyFunc func(c *gin.Context) string) gin.HandlerFunc {
	limiter := &RateLimiter{
		rdb:     rdb,
		rate:    rate,
		window:  window,
		keyFunc: keyFunc,
	}

	return func(c *gin.Context) {
		key := limiter.keyFunc(c)
		
		ctx := context.Background()
		
		current, err := limiter.rdb.Get(ctx, key).Result()
		if err != nil && err != redis.Nil {
			c.Next()
			return
		}

		var count int
		if current != "" {
			count, _ = strconv.Atoi(current)
		}

		if count >= limiter.rate {
			c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", limiter.rate))
			c.Header("X-RateLimit-Remaining", "0")
			c.Header("X-RateLimit-Reset", fmt.Sprintf("%d", time.Now().Add(limiter.window).Unix()))
			
			response.BadRequest(c, "Rate limit exceeded")
			c.AbortWithStatus(http.StatusTooManyRequests)
			return
		}

		pipe := limiter.rdb.Pipeline()
		pipe.Incr(ctx, key)
		if count == 0 {
			pipe.Expire(ctx, key, limiter.window)
		}
		pipe.Exec(ctx)

		c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", limiter.rate))
		c.Header("X-RateLimit-Remaining", fmt.Sprintf("%d", limiter.rate-count-1))
		
		c.Next()
	}
}