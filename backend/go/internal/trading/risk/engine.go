package risk

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/hibiken/asynq"
	"github.com/redis/go-redis/v9"
	"github.com/shopspring/decimal"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

// RiskConfig holds risk management parameters for a portfolio.
type RiskConfig struct {
	MaxPositionSize    decimal.Decimal `json:"max_position_size"`
	MaxDrawdownPercent decimal.Decimal `json:"max_drawdown_percent"`
	MaxDailyLoss       decimal.Decimal `json:"max_daily_loss"`
	MaxOpenPositions   int             `json:"max_open_positions"`
	MaxLeverage        decimal.Decimal `json:"max_leverage"`
	StopLossRequired   bool            `json:"stop_loss_required"`
}

// RiskCheckResult contains the result of a risk evaluation.
type RiskCheckResult struct {
	Allowed    bool     `json:"allowed"`
	Violations []string `json:"violations"`
	RiskScore  float64  `json:"risk_score"`
	Timestamp  string   `json:"timestamp"`
}

// OrderRiskRequest represents a request to check risk before placing an order.
type OrderRiskRequest struct {
	UserID      string          `json:"user_id"`
	PortfolioID string          `json:"portfolio_id"`
	Symbol      string          `json:"symbol"`
	Side        string          `json:"side"`
	Quantity    decimal.Decimal `json:"quantity"`
	Price       decimal.Decimal `json:"price"`
	Leverage    decimal.Decimal `json:"leverage"`
	HasStopLoss bool            `json:"has_stop_loss"`
}

// PortfolioRiskReport provides an overall risk assessment for a portfolio.
type PortfolioRiskReport struct {
	PortfolioID       string          `json:"portfolio_id"`
	TotalExposure     decimal.Decimal `json:"total_exposure"`
	UsedMargin        decimal.Decimal `json:"used_margin"`
	MarginUtilization decimal.Decimal `json:"margin_utilization"`
	CurrentDrawdown   decimal.Decimal `json:"current_drawdown"`
	OpenPositions     int             `json:"open_positions"`
	RiskScore         float64         `json:"risk_score"`
	Status            string          `json:"status"`
	Timestamp         string          `json:"timestamp"`
}

// DefaultRiskConfig returns sensible defaults for risk management.
func DefaultRiskConfig() *RiskConfig {
	return &RiskConfig{
		MaxPositionSize:    decimal.NewFromFloat(10000),
		MaxDrawdownPercent: decimal.NewFromFloat(15),
		MaxDailyLoss:       decimal.NewFromFloat(5000),
		MaxOpenPositions:   20,
		MaxLeverage:        decimal.NewFromFloat(10),
		StopLossRequired:   true,
	}
}

type Engine struct {
	db     *gorm.DB
	rdb    *redis.Client
	logger *zap.Logger
}

func NewEngine(db *gorm.DB, rdb *redis.Client, logger *zap.Logger) *Engine {
	return &Engine{db: db, rdb: rdb, logger: logger}
}

// CheckOrderRisk validates an order against risk management rules.
func (e *Engine) CheckOrderRisk(ctx context.Context, req *OrderRiskRequest) (*RiskCheckResult, error) {
	config := e.loadRiskConfig(ctx, req.UserID)
	result := &RiskCheckResult{
		Allowed:   true,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
	}

	orderValue := req.Quantity.Mul(req.Price)

	// Check position size limit
	if orderValue.GreaterThan(config.MaxPositionSize) {
		result.Violations = append(result.Violations,
			fmt.Sprintf("Order value %s exceeds max position size %s", orderValue.String(), config.MaxPositionSize.String()))
	}

	// Check leverage limit
	if req.Leverage.GreaterThan(config.MaxLeverage) {
		result.Violations = append(result.Violations,
			fmt.Sprintf("Leverage %s exceeds max leverage %s", req.Leverage.String(), config.MaxLeverage.String()))
	}

	// Check stop-loss requirement
	if config.StopLossRequired && !req.HasStopLoss {
		result.Violations = append(result.Violations, "Stop-loss order is required but not set")
	}

	// Check daily loss limit
	dailyLoss, err := e.getDailyLoss(ctx, req.UserID)
	if err == nil && dailyLoss.Abs().GreaterThan(config.MaxDailyLoss) {
		result.Violations = append(result.Violations,
			fmt.Sprintf("Daily loss %s exceeds limit %s", dailyLoss.String(), config.MaxDailyLoss.String()))
	}

	// Check max open positions
	openCount, err := e.getOpenPositionCount(ctx, req.UserID)
	if err == nil && openCount >= config.MaxOpenPositions {
		result.Violations = append(result.Violations,
			fmt.Sprintf("Open positions %d at maximum %d", openCount, config.MaxOpenPositions))
	}

	if len(result.Violations) > 0 {
		result.Allowed = false
		result.RiskScore = float64(len(result.Violations)) * 25.0
		if result.RiskScore > 100 {
			result.RiskScore = 100
		}
	}

	return result, nil
}

// GetPortfolioRisk generates a risk report for a portfolio.
func (e *Engine) GetPortfolioRisk(ctx context.Context, userID, portfolioID string) (*PortfolioRiskReport, error) {
	report := &PortfolioRiskReport{
		PortfolioID: portfolioID,
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
	}

	// Get open position count
	openCount, _ := e.getOpenPositionCount(ctx, userID)
	report.OpenPositions = openCount

	// Calculate risk score based on metrics
	var riskScore float64
	config := e.loadRiskConfig(ctx, userID)

	posRatio := float64(openCount) / float64(config.MaxOpenPositions) * 100
	riskScore += posRatio * 0.3

	dailyLoss, _ := e.getDailyLoss(ctx, userID)
	if !config.MaxDailyLoss.IsZero() {
		lossRatio := dailyLoss.Abs().Div(config.MaxDailyLoss).InexactFloat64() * 100
		riskScore += lossRatio * 0.4
	}

	riskScore += 10 // Base risk score

	if riskScore > 100 {
		riskScore = 100
	}

	report.RiskScore = riskScore
	report.TotalExposure = decimal.Zero
	report.UsedMargin = decimal.Zero
	report.MarginUtilization = decimal.Zero
	report.CurrentDrawdown = dailyLoss.Abs()

	switch {
	case riskScore < 30:
		report.Status = "low"
	case riskScore < 60:
		report.Status = "medium"
	case riskScore < 80:
		report.Status = "high"
	default:
		report.Status = "critical"
	}

	return report, nil
}

// HandleRiskCheckTask processes asynchronous risk check tasks from the queue.
func (e *Engine) HandleRiskCheckTask(ctx context.Context, t *asynq.Task) error {
	e.logger.Info("Processing risk check task", zap.String("type", t.Type()))

	var req OrderRiskRequest
	if err := json.Unmarshal(t.Payload(), &req); err != nil {
		e.logger.Error("Failed to unmarshal risk check task", zap.Error(err))
		return err
	}

	result, err := e.CheckOrderRisk(ctx, &req)
	if err != nil {
		e.logger.Error("Risk check failed", zap.Error(err))
		return err
	}

	if !result.Allowed {
		e.logger.Warn("Order rejected by risk engine",
			zap.String("user_id", req.UserID),
			zap.Strings("violations", result.Violations),
		)
	}

	return nil
}

// loadRiskConfig loads user-specific risk config from Redis or returns defaults.
func (e *Engine) loadRiskConfig(ctx context.Context, userID string) *RiskConfig {
	key := fmt.Sprintf("risk:config:%s", userID)
	data, err := e.rdb.Get(ctx, key).Bytes()
	if err != nil {
		return DefaultRiskConfig()
	}

	var config RiskConfig
	if err := json.Unmarshal(data, &config); err != nil {
		return DefaultRiskConfig()
	}
	return &config
}

// SaveRiskConfig persists a user's risk configuration in Redis.
func (e *Engine) SaveRiskConfig(ctx context.Context, userID string, config *RiskConfig) error {
	if config == nil {
		return errors.New("config cannot be nil")
	}
	key := fmt.Sprintf("risk:config:%s", userID)
	data, err := json.Marshal(config)
	if err != nil {
		return err
	}
	return e.rdb.Set(ctx, key, data, 0).Err()
}

// getDailyLoss returns the total realized loss for today from Redis cache.
func (e *Engine) getDailyLoss(ctx context.Context, userID string) (decimal.Decimal, error) {
	key := fmt.Sprintf("risk:daily_loss:%s:%s", userID, time.Now().UTC().Format("2006-01-02"))
	val, err := e.rdb.Get(ctx, key).Result()
	if err != nil {
		return decimal.Zero, err
	}
	return decimal.NewFromString(val)
}

// getOpenPositionCount returns the number of currently open positions.
func (e *Engine) getOpenPositionCount(ctx context.Context, userID string) (int, error) {
	var count int64
	err := e.db.WithContext(ctx).Table("positions").
		Where("user_id = ? AND status = ?", userID, "open").
		Count(&count).Error
	return int(count), err
}
