CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS municipal_services (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    tariff_amount DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    service_id BIGINT,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

MERGE INTO municipal_services (id, service_name, service_type, tariff_amount)
KEY(id)
VALUES
    (1, 'Istanbul Transit Micro-Payment', 'TRANSIT', 17.70),
    (2, 'Municipal Water Utility Bill', 'UTILITY', 150.00),
    (3, 'Smart Parking Meter Zone A', 'PARKING', 40.00),
    (4, 'Natural Gas Utility Bill', 'UTILITY', 485.50);
