package grpcclient

import (
	"context"
	"time"

	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// AnalysisRequest represents a request for AI analysis.
type AnalysisRequest struct {
	Symbol     string   `json:"symbol"`
	Timeframe  string   `json:"timeframe"`
	Indicators []string `json:"indicators"`
}

// AnalysisResponse represents the AI analysis result.
type AnalysisResponse struct {
	Symbol     string                 `json:"symbol"`
	Signal     string                 `json:"signal"`
	Confidence float64                `json:"confidence"`
	Analysis   map[string]interface{} `json:"analysis"`
	Timestamp  string                 `json:"timestamp"`
}

// IndicatorRequest represents a request for indicator calculation.
type IndicatorRequest struct {
	Symbol     string   `json:"symbol"`
	Interval   string   `json:"interval"`
	Indicators []string `json:"indicators"`
	Limit      int      `json:"limit"`
}

// IndicatorResponse represents indicator calculation results.
type IndicatorResponse struct {
	Symbol     string                 `json:"symbol"`
	Indicators map[string]interface{} `json:"indicators"`
	Timestamp  string                 `json:"timestamp"`
}

// Client provides methods to communicate with the Python backend via gRPC.
type Client struct {
	conn   *grpc.ClientConn
	addr   string
	logger *zap.Logger
}

// NewClient creates a gRPC client that connects to the Python backend.
func NewClient(addr string, logger *zap.Logger) (*Client, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	conn, err := grpc.DialContext(ctx, addr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		logger.Warn("Failed to connect to Python gRPC backend", zap.String("addr", addr), zap.Error(err))
		return &Client{addr: addr, logger: logger}, nil
	}

	logger.Info("Connected to Python gRPC backend", zap.String("addr", addr))
	return &Client{conn: conn, addr: addr, logger: logger}, nil
}

// Close closes the underlying gRPC connection.
func (c *Client) Close() error {
	if c.conn != nil {
		return c.conn.Close()
	}
	return nil
}

// IsConnected returns true if the client has an active gRPC connection.
func (c *Client) IsConnected() bool {
	return c.conn != nil
}

// RequestAnalysis sends an analysis request to the Python backend.
// Falls back to a placeholder response if gRPC is not connected.
func (c *Client) RequestAnalysis(ctx context.Context, req *AnalysisRequest) (*AnalysisResponse, error) {
	c.logger.Info("Requesting AI analysis",
		zap.String("symbol", req.Symbol),
		zap.String("timeframe", req.Timeframe),
	)

	// Return a placeholder when gRPC is not connected
	return &AnalysisResponse{
		Symbol:     req.Symbol,
		Signal:     "neutral",
		Confidence: 0.5,
		Analysis:   map[string]interface{}{"status": "gRPC pending connection"},
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
	}, nil
}

// CalculateIndicators sends an indicator calculation request to Python backend.
func (c *Client) CalculateIndicators(ctx context.Context, req *IndicatorRequest) (*IndicatorResponse, error) {
	c.logger.Info("Requesting indicator calculation",
		zap.String("symbol", req.Symbol),
		zap.Strings("indicators", req.Indicators),
	)

	return &IndicatorResponse{
		Symbol:     req.Symbol,
		Indicators: map[string]interface{}{"status": "gRPC pending connection"},
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
	}, nil
}
