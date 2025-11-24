-- Продавцы извлечённые из seller.ibd
-- Создано автоматически

USE enb;

-- Создание таблицы
CREATE TABLE IF NOT EXISTS seller (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    user_id INT,
    company_id INT,
    status INT DEFAULT 1,
    created_at INT,
    updated_at INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Вставка данных
