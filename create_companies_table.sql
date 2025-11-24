CREATE TABLE IF NOT EXISTS companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description TEXT,
    user_id INT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    logo VARCHAR(255),
    status INT,
    created_at INT,
    updated_at INT,
    category_id INT
) ENGINE=InnoDB ROW_FORMAT=COMPACT;
