-- Step 1: Insert 10 random users into the 'users' table
INSERT INTO TEST_BMS.test_users (first_name, last_name, email, password_hash, phone_number, dob, status)
VALUES 
('Alice', 'Smith', 'alice.smith@example.com', 'hashed_password_1', '9876543210', '1990-03-12', 'active'),
('Bob', 'Johnson', 'bob.johnson@example.com', 'hashed_password_2', '9123456789', '1988-05-23', 'inactive'),
('Charlie', 'Brown', 'charlie.brown@example.com', 'hashed_password_3', '9234567890', '1995-07-30', 'active'),
('David', 'Williams', 'david.williams@example.com', 'hashed_password_4', '9345678901', '1987-02-18', 'suspended'),
('Eva', 'Jones', 'eva.jones@example.com', 'hashed_password_5', '9456789012', '1992-08-25', 'active'),
('Frank', 'Garcia', 'frank.garcia@example.com', 'hashed_password_6', '9567890123', '1989-11-05', 'inactive'),
('Grace', 'Martinez', 'grace.martinez@example.com', 'hashed_password_7', '9678901234', '1993-12-14', 'active'),
('Hank', 'Rodriguez', 'hank.rodriguez@example.com', 'hashed_password_8', '9789012345', '1986-01-22', 'active'),
('Ivy', 'Wilson', 'ivy.wilson@example.com', 'hashed_password_9', '9890123456', '1994-04-10', 'suspended'),
('Jack', 'Moore', 'jack.moore@example.com', 'hashed_password_10', '9901234567', '1991-09-03', 'active');

-- Step 2: Display all the users to verify the inserts
SELECT * FROM TEST_BMS.test_users;
