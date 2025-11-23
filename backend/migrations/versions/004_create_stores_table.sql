-- Create stores table with PostGIS
-- Migration: 004_create_stores_table

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    working_hours VARCHAR(255),
    description TEXT,
    location GEOMETRY(POINT, 4326) NOT NULL,
    delivery_zone GEOMETRY(POLYGON, 4326),
    image VARCHAR(500),
    is_active VARCHAR(10) DEFAULT 'true',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stores_name ON stores(name);
CREATE INDEX idx_stores_location ON stores USING GIST(location);
CREATE INDEX idx_stores_delivery_zone ON stores USING GIST(delivery_zone);

-- Comments
COMMENT ON TABLE stores IS 'Магазины с геолокацией (PostGIS)';
COMMENT ON COLUMN stores.location IS 'Координаты магазина (POINT)';
COMMENT ON COLUMN stores.delivery_zone IS 'Зона доставки (POLYGON)';
COMMENT ON COLUMN stores.working_hours IS 'Время работы, например: 8:00 - 22:00';
