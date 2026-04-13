package order

import (
	"context"
	"strconv"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend-go/internal/trading/exchange"
)

type Service struct {
	db      *gorm.DB
	rdb     *redis.Client
	factory *exchange.Factory
}

func NewService(db *gorm.DB, rdb *redis.Client) *Service {
	return &Service{
		db:      db,
		rdb:     rdb,
		factory: exchange.NewFactory(),
	}
}

func (s *Service) CreateOrder(ctx context.Context, order *Order) (*Order, error) {
	// Generate client order ID
	order.ClientOrderID = uuid.New().String()

	// Save order to database first
	if err := s.db.WithContext(ctx).Create(order).Error; err != nil {
		return nil, err
	}

	// Get exchange adapter and submit order
	adapter, err := s.factory.CreateAdapter(order.Exchange, "", "") // TODO: Get API keys from user settings
	if err != nil {
		return nil, err
	}

	exchangeReq := &exchange.OrderRequest{
		Symbol:      order.Symbol,
		Side:        order.Side,
		Type:        order.Type,
		Quantity:    order.Quantity,
		Price:       order.Price,
		StopPrice:   order.StopPrice,
		TimeInForce: order.TimeInForce,
	}

	exchangeResp, err := adapter.CreateOrder(ctx, exchangeReq)
	if err != nil {
		// Update order status to rejected
		order.Status = "REJECTED"
		s.db.WithContext(ctx).Save(order)
		return nil, err
	}

	// Update order with exchange response
	order.ExchangeOrderID = exchangeResp.OrderID
	order.Status = exchangeResp.Status
	order.ExecutedQty = exchangeResp.ExecutedQty

	if err := s.db.WithContext(ctx).Save(order).Error; err != nil {
		return nil, err
	}

	return order, nil
}

func (s *Service) ListOrders(ctx context.Context, userID, pageStr, limitStr, symbol, status, exchange string) ([]*Order, int64, error) {
	page, err := strconv.Atoi(pageStr)
	if err != nil {
		page = 1
	}

	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 20
	}

	offset := (page - 1) * limit

	query := s.db.WithContext(ctx).Where("user_id = ?", userID)

	if symbol != "" {
		query = query.Where("symbol = ?", symbol)
	}
	if status != "" {
		query = query.Where("status = ?", status)
	}
	if exchange != "" {
		query = query.Where("exchange = ?", exchange)
	}

	var orders []*Order
	err = query.Order("created_at DESC").Limit(limit).Offset(offset).Find(&orders).Error
	if err != nil {
		return nil, 0, err
	}

	var total int64
	countQuery := s.db.WithContext(ctx).Model(&Order{}).Where("user_id = ?", userID)
	if symbol != "" {
		countQuery = countQuery.Where("symbol = ?", symbol)
	}
	if status != "" {
		countQuery = countQuery.Where("status = ?", status)
	}
	if exchange != "" {
		countQuery = countQuery.Where("exchange = ?", exchange)
	}

	err = countQuery.Count(&total).Error
	return orders, total, err
}

func (s *Service) GetOrder(ctx context.Context, userID, orderID string) (*Order, error) {
	var order Order
	err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", orderID, userID).First(&order).Error
	return &order, err
}

func (s *Service) CancelOrder(ctx context.Context, userID, orderID string) error {
	var order Order
	if err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", orderID, userID).First(&order).Error; err != nil {
		return err
	}

	// Get exchange adapter and cancel order
	adapter, err := s.factory.CreateAdapter(order.Exchange, "", "") // TODO: Get API keys from user settings
	if err != nil {
		return err
	}

	if err := adapter.CancelOrder(ctx, order.ExchangeOrderID); err != nil {
		return err
	}

	// Update order status
	order.Status = "CANCELED"
	return s.db.WithContext(ctx).Save(&order).Error
}

func (s *Service) UpdateOrderStatus(ctx context.Context, userID, orderID, status string) error {
	return s.db.WithContext(ctx).Model(&Order{}).
		Where("id = ? AND user_id = ?", orderID, userID).
		Update("status", status).Error
}

func (s *Service) GetActiveOrders(ctx context.Context, userID string) ([]*Order, error) {
	var orders []*Order
	err := s.db.WithContext(ctx).
		Where("user_id = ? AND status IN (?)", userID, []string{"NEW", "PARTIALLY_FILLED"}).
		Order("created_at DESC").
		Find(&orders).Error
	return orders, err
}

func (s *Service) GetOrderHistory(ctx context.Context, userID, pageStr, limitStr string) ([]*Order, int64, error) {
	page, err := strconv.Atoi(pageStr)
	if err != nil {
		page = 1
	}

	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 50
	}

	offset := (page - 1) * limit

	var orders []*Order
	err = s.db.WithContext(ctx).
		Where("user_id = ? AND status IN (?)", userID, []string{"FILLED", "CANCELED", "REJECTED"}).
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&orders).Error

	if err != nil {
		return nil, 0, err
	}

	var total int64
	err = s.db.WithContext(ctx).Model(&Order{}).
		Where("user_id = ? AND status IN (?)", userID, []string{"FILLED", "CANCELED", "REJECTED"}).
		Count(&total).Error

	return orders, total, err
}