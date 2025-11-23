-- Create orders and order_items tables
-- Migration: 005_create_orders_tables

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(50) NOT NULL DEFAULT 'created',
    total NUMERIC(10, 2) NOT NULL,
    delivery_address VARCHAR(500) NOT NULL,
    delivery_time TIMESTAMP,
    delivery_comment TEXT,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    contact_phone VARCHAR(20) NOT NULL,
    contact_name VARCHAR(255) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    product_image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Comments
COMMENT ON TABLE orders IS 'Заказы пользователей';
COMMENT ON COLUMN orders.status IS 'Статус: created, paid, processing, delivering, completed, cancelled';
COMMENT ON COLUMN orders.payment_method IS 'Способ оплаты: card, cash, online';
COMMENT ON COLUMN orders.payment_status IS 'Статус оплаты: pending, paid, failed';

COMMENT ON TABLE order_items IS 'Товары в заказе';
COMMENT ON COLUMN order_items.price IS 'Цена на момент заказа (фиксируется)';
COMMENT ON COLUMN order_items.product_name IS 'Название товара (на случай удаления товара)';
