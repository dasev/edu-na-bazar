-- Create categories table
-- Migration: 002_create_categories_table

CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    icon VARCHAR(50),
    description VARCHAR(1000),
    parent_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_name ON categories(name);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);

-- Comments
COMMENT ON TABLE categories IS 'Категории товаров';
COMMENT ON COLUMN categories.slug IS 'URL-friendly название';
COMMENT ON COLUMN categories.parent_id IS 'Родительская категория для иерархии';
COMMENT ON COLUMN categories.sort_order IS 'Порядок сортировки';
