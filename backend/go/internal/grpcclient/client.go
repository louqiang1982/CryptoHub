package grpcclient

import (
	"context"
	"time"

	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "github.com/louqiang1982/CryptoHub/backend/go/proto/pb"
)

// AnalysisRequest represents a request for AI analysis.
type AnalysisRequest struct {
	Symbol     string   `json:"symbol"`
	Timeframe  string   `json:"timeframe"`
	Indicators []string `json:"indicators"`
}

// AnalysisResponse represents the AI analysis result.
type AnalysisResponse struct {
	Symbol          string             `json:"symbol"`
	Signal          string             `json:"signal"`
	Confidence      float64            `json:"confidence"`
	Summary         string             `json:"summary"`
	IndicatorValues map[string]float64 `json:"indicator_values"`
	Analysis        map[string]interface{} `json:"analysis"`
	Timestamp       string             `json:"timestamp"`
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
	conn              *grpc.ClientConn
	addr              string
	logger            *zap.Logger
	analysisClient    pb.AnalysisServiceClient
	indicatorClient   pb.IndicatorServiceClient
	marketDataClient  pb.MarketDataServiceClient
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
	return &Client{
		conn:             conn,
		addr:             addr,
		logger:           logger,
		analysisClient:   pb.NewAnalysisServiceClient(conn),
		indicatorClient:  pb.NewIndicatorServiceClient(conn),
		marketDataClient: pb.NewMarketDataServiceClient(conn),
	}, nil
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

	if !c.IsConnected() {
		return &AnalysisResponse{
			Symbol:     req.Symbol,
			Signal:     "neutral",
			Confidence: 0.5,
			Analysis:   map[string]interface{}{"status": "gRPC not connected"},
			Timestamp:  time.Now().UTC().Format(time.RFC3339),
		}, nil
	}

	resp, err := c.analysisClient.GetAnalysis(ctx, &pb.AnalysisReq{
		Symbol:     req.Symbol,
		Timeframe:  req.Timeframe,
		Indicators: req.Indicators,
	})
	if err != nil {
		c.logger.Error("gRPC GetAnalysis failed", zap.Error(err))
		return &AnalysisResponse{
			Symbol:     req.Symbol,
			Signal:     "neutral",
			Confidence: 0.5,
			Analysis:   map[string]interface{}{"error": err.Error()},
			Timestamp:  time.Now().UTC().Format(time.RFC3339),
		}, nil
	}

	return &AnalysisResponse{
		Symbol:          resp.Symbol,
		Signal:          resp.Signal,
		Confidence:      resp.Confidence,
		Summary:         resp.Summary,
		IndicatorValues: resp.IndicatorValues,
		Analysis:        map[string]interface{}{"summary": resp.Summary},
		Timestamp:       resp.Timestamp,
	}, nil
}

// CalculateIndicators sends an indicator calculation request to Python backend.
func (c *Client) CalculateIndicators(ctx context.Context, req *IndicatorRequest) (*IndicatorResponse, error) {
	c.logger.Info("Requesting indicator calculation",
		zap.String("symbol", req.Symbol),
		zap.Strings("indicators", req.Indicators),
	)

	if !c.IsConnected() {
		return &IndicatorResponse{
			Symbol:     req.Symbol,
			Indicators: map[string]interface{}{"status": "gRPC not connected"},
			Timestamp:  time.Now().UTC().Format(time.RFC3339),
		}, nil
	}

	params := make([]*pb.IndicatorParam, 0, len(req.Indicators))
	for _, ind := range req.Indicators {
		params = append(params, &pb.IndicatorParam{
			Type:   ind,
			Period: 14,
		})
	}

	resp, err := c.indicatorClient.Calculate(ctx, &pb.IndicatorReq{
		Symbol:     req.Symbol,
		Interval:   req.Interval,
		Indicators: params,
		Limit:      int32(req.Limit),
	})
	if err != nil {
		c.logger.Error("gRPC Calculate failed", zap.Error(err))
		return &IndicatorResponse{
			Symbol:     req.Symbol,
			Indicators: map[string]interface{}{"error": err.Error()},
			Timestamp:  time.Now().UTC().Format(time.RFC3339),
		}, nil
	}

	indicators := make(map[string]interface{})
	for _, v := range resp.Indicators {
		indicators[v.Type] = v.Values
	}

	return &IndicatorResponse{
		Symbol:     resp.Symbol,
		Indicators: indicators,
		Timestamp:  resp.Timestamp,
	}, nil
}

// GetKlines fetches historical kline data from the Python backend via gRPC.
func (c *Client) GetKlines(ctx context.Context, symbol, interval string, limit int) (*pb.KlineResp, error) {
	if !c.IsConnected() {
		return &pb.KlineResp{Symbol: symbol, Interval: interval}, nil
	}

	return c.marketDataClient.GetKlines(ctx, &pb.KlineReq{
		Symbol:   symbol,
		Interval: interval,
		Limit:    int32(limit),
	})
}
