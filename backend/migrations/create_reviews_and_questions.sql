-- Создание таблиц для отзывов и вопросов

-- Таблица отзывов о товарах
CREATE TABLE IF NOT EXISTS market.product_reviews (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    comment TEXT NOT NULL,
    advantages TEXT,
    disadvantages TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_count INTEGER DEFAULT 0,
    not_helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT valid_rating CHECK (rating BETWEEN 1 AND 5)
);

-- Таблица ответов продавца на отзывы
CREATE TABLE IF NOT EXISTS market.review_responses (
    id BIGSERIAL PRIMARY KEY,
    review_id BIGINT NOT NULL REFERENCES market.product_reviews(id) ON DELETE CASCADE,
    store_id BIGINT REFERENCES market.stores(id) ON DELETE CASCADE,
    response_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица вопросов о товарах
CREATE TABLE IF NOT EXISTS market.product_questions (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES market.products(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица ответов на вопросы
CREATE TABLE IF NOT EXISTS market.question_answers (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL REFERENCES market.product_questions(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES config.users(id) ON DELETE SET NULL,
    store_id BIGINT REFERENCES market.stores(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_seller BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица для отслеживания полезности отзывов (лайки/дизлайки)
CREATE TABLE IF NOT EXISTS market.review_votes (
    id BIGSERIAL PRIMARY KEY,
    review_id BIGINT NOT NULL REFERENCES market.product_reviews(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES config.users(id) ON DELETE CASCADE,
    is_helpful BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(review_id, user_id)
);

-- Индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_product_reviews_product_id ON market.product_reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_product_reviews_user_id ON market.product_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_product_reviews_rating ON market.product_reviews(rating);
CREATE INDEX IF NOT EXISTS idx_product_reviews_created_at ON market.product_reviews(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_review_responses_review_id ON market.review_responses(review_id);
CREATE INDEX IF NOT EXISTS idx_review_responses_store_id ON market.review_responses(store_id);

CREATE INDEX IF NOT EXISTS idx_product_questions_product_id ON market.product_questions(product_id);
CREATE INDEX IF NOT EXISTS idx_product_questions_user_id ON market.product_questions(user_id);
CREATE INDEX IF NOT EXISTS idx_product_questions_created_at ON market.product_questions(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_question_answers_question_id ON market.question_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_question_answers_user_id ON market.question_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_question_answers_store_id ON market.question_answers(store_id);

CREATE INDEX IF NOT EXISTS idx_review_votes_review_id ON market.review_votes(review_id);
CREATE INDEX IF NOT EXISTS idx_review_votes_user_id ON market.review_votes(user_id);

-- Комментарии
COMMENT ON TABLE market.product_reviews IS 'Отзывы покупателей о товарах';
COMMENT ON TABLE market.review_responses IS 'Ответы продавцов на отзывы';
COMMENT ON TABLE market.product_questions IS 'Вопросы покупателей о товарах';
COMMENT ON TABLE market.question_answers IS 'Ответы на вопросы (от продавцов или других покупателей)';
COMMENT ON TABLE market.review_votes IS 'Оценки полезности отзывов (лайки/дизлайки)';
