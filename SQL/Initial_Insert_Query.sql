-- Step 1: Create the schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS TEST_BMS;

-- Step 2: Use the 'BMS' schema
USE TEST_BMS;

-- Step 3: Create the 'users' table inside the 'BMS' schema
CREATE TABLE IF NOT EXISTS test_users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    dob DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active'
);

-- Step 4: Insert a test value into the 'users' table
INSERT INTO test_bms.test_users (first_name, last_name, email, password_hash, phone_number, dob, status)
VALUES ('John', 'Doe', 'john.doe@example.com', 'hashed_password_123', '1234567890', '1985-07-15', 'active');

-- Step 5: Display the inserted value
SELECT * FROM TEST_BMS.test_users;
