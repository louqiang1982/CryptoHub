-- Drop all indexes first
DROP INDEX IF EXISTS idx_klines_unique;
DROP INDEX IF EXISTS idx_klines_open_time;
DROP INDEX IF EXISTS idx_klines_symbol_interval;

DROP INDEX IF EXISTS idx_subscriptions_status;
DROP INDEX IF EXISTS idx_subscriptions_user_id;

DROP INDEX IF EXISTS idx_notifications_created_at;
DROP INDEX IF EXISTS idx_notifications_status;
DROP INDEX IF EXISTS idx_notifications_user_id;

DROP INDEX IF EXISTS idx_api_keys_exchange;
DROP INDEX IF EXISTS idx_api_keys_user_id;

DROP INDEX IF EXISTS idx_portfolios_user_id;

DROP INDEX IF EXISTS idx_positions_status;
DROP INDEX IF EXISTS idx_positions_symbol;
DROP INDEX IF EXISTS idx_positions_strategy_id;
DROP INDEX IF EXISTS idx_positions_user_id;

DROP INDEX IF EXISTS idx_orders_created_at;
DROP INDEX IF EXISTS idx_orders_status;
DROP INDEX IF EXISTS idx_orders_symbol;
DROP INDEX IF EXISTS idx_orders_exchange;
DROP INDEX IF EXISTS idx_orders_strategy_id;
DROP INDEX IF EXISTS idx_orders_user_id;

DROP INDEX IF EXISTS idx_strategies_status;
DROP INDEX IF EXISTS idx_strategies_user_id;

DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_username;
DROP INDEX IF EXISTS idx_users_email;

-- Drop all tables
DROP TABLE IF EXISTS klines;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS api_keys;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS users;