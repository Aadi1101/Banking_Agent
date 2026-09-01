use bms;

-- Table for signup/login data
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each user
    Username VARCHAR(255) NOT NULL UNIQUE, -- Username for login
    PasswordHash VARCHAR(255) NOT NULL,   -- Encrypted password
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Account creation time
);


-- Table for user personal details
CREATE TABLE UserDetails (
    UserDetailID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for user details
    UserID INT NOT NULL, -- Foreign key to Users table
    State VARCHAR(100) NOT NULL, -- User's state (Indian states)
    City VARCHAR(100) NOT NULL,  -- User's city
    Pincode VARCHAR(10) NOT NULL, -- User's pincode
    Address TEXT, -- Optional full address (in our case, Address is not being used)
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Table for payment/transaction-related information
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY, -- Unique transaction ID
    UserID INT NOT NULL, -- Foreign key to Users table
    Amount DECIMAL(15, 2) NOT NULL, -- Amount of transaction
    TransactionType ENUM('Credit', 'Debit') NOT NULL, -- Type of transaction (Credit/Debit)
    TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of transaction
    Description TEXT, -- Details of transaction
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Table for savings of users
CREATE TABLE Savings (
    SavingsID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for savings record
    UserID INT NOT NULL, -- Foreign key to Users table
    Balance DECIMAL(15, 2) NOT NULL DEFAULT 0, -- Current savings balance
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Last update time
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Table for loans issued by the user
CREATE TABLE Loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY, -- Unique loan ID
    UserID INT NOT NULL, -- Foreign key to Users table
    LoanAmount DECIMAL(15, 2) NOT NULL, -- Loan amount
    LoanType VARCHAR(100) NOT NULL, -- Loan type (e.g., "Home Loan", "Car Loan")
    IssuedDate DATE NOT NULL, -- Loan issuance date
    DueDate DATE NOT NULL, -- Loan due date
    Status ENUM('Active', 'Closed', 'Defaulted') NOT NULL DEFAULT 'Active', -- Loan status
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Table for stock investments of users
CREATE TABLE Investments (
    InvestmentID INT AUTO_INCREMENT PRIMARY KEY, -- Unique investment ID
    UserID INT NOT NULL, -- Foreign key to Users table
    StockSymbol VARCHAR(20) NOT NULL, -- Stock symbol (e.g., "AAPL")
    Shares INT NOT NULL, -- Number of shares
    PurchasePrice DECIMAL(10, 2) NOT NULL, -- Purchase price per share
    PurchaseDate DATE NOT NULL, -- Date of purchase
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Table for donations made by users to the bank
CREATE TABLE Donations (
    DonationID INT AUTO_INCREMENT PRIMARY KEY, -- Unique donation ID
    UserID INT NOT NULL, -- Foreign key to Users table
    Amount DECIMAL(15, 2) NOT NULL, -- Donation amount
    DonationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of donation
    Note TEXT, -- Optional note
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);


-- Table for blocked accounts
CREATE TABLE BlockedAccounts (
    BlockID INT AUTO_INCREMENT PRIMARY KEY, -- Unique block ID
    UserID INT NOT NULL, -- Foreign key to Users table
    BlockReason TEXT NOT NULL, -- Reason for blocking
    BlockDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date when the account was blocked
    Status TINYINT(1) NOT NULL DEFAULT 1, -- Status: 1 for blocked, 0 for unblocked
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- View for calculating total balance dynamically
CREATE OR REPLACE VIEW UserTotalBalance AS
SELECT 
    u.UserID,
    u.Username,
    COALESCE(s.Balance, 0) AS SavingsBalance, -- Balance from Savings table
    COALESCE(SUM(i.Shares * i.PurchasePrice), 0) AS InvestmentBalance, -- Total value of investments
    COALESCE(s.Balance, 0) + COALESCE(SUM(i.Shares * i.PurchasePrice), 0) AS TotalBalance -- Total of all balances
FROM 
    Users u
LEFT JOIN 
    Savings s ON u.UserID = s.UserID
LEFT JOIN 
    Investments i ON u.UserID = i.UserID
GROUP BY 
    u.UserID;
    
    
-- Insert 10 rows of sample data into Users table (signup/login data)
INSERT INTO Users (Username, PasswordHash) VALUES
('john_doe', 'hashed_password_1'),
('jane_smith', 'hashed_password_2'),
('bob_jones', 'hashed_password_3'),
('alice_williams', 'hashed_password_4'),
('charles_brown', 'hashed_password_5'),
('mary_johnson', 'hashed_password_6'),
('david_martin', 'hashed_password_7'),
('emily_davis', 'hashed_password_8'),
('frank_white', 'hashed_password_9'),
('grace_green', 'hashed_password_10');

-- Insert 10 rows of sample data into UserDetails table (personal details with different states and cities)
INSERT INTO UserDetails (UserID, State, City, Pincode) VALUES
(1, 'Maharashtra', 'Mumbai', '400001'),
(2, 'Delhi', 'New Delhi', '110001'),
(3, 'Karnataka', 'Bengaluru', '560001'),
(4, 'Tamil Nadu', 'Chennai', '600001'),
(5, 'West Bengal', 'Kolkata', '700001'),
(6, 'Uttar Pradesh', 'Lucknow', '226001'),
(7, 'Kerala', 'Kochi', '682001'),
(8, 'Punjab', 'Chandigarh', '160001'),
(9, 'Rajasthan', 'Jaipur', '302001'),
(10, 'Gujarat', 'Ahmedabad', '380001');

-- Insert 10 rows of sample data into Transactions table (payment/transaction-related info)
INSERT INTO Transactions (UserID, Amount, TransactionType, Description) VALUES
(1, 1000.00, 'Credit', 'Deposit to savings account'),
(2, 500.00, 'Debit', 'Payment for car loan'),
(3, 2000.00, 'Credit', 'Salary deposit'),
(4, 1500.00, 'Debit', 'Grocery shopping'),
(5, 2500.00, 'Credit', 'Bank transfer from savings'),
(6, 1200.00, 'Debit', 'Utility bill payment'),
(7, 3000.00, 'Credit', 'Investment return'),
(8, 800.00, 'Debit', 'Loan repayment'),
(9, 4500.00, 'Credit', 'Salary deposit'),
(10, 350.00, 'Debit', 'Medical expenses');

-- Insert 10 rows of sample data into Savings table (user savings balances)
INSERT INTO Savings (UserID, Balance) VALUES
(1, 5000.00),
(2, 3000.00),
(3, 7000.00),
(4, 2500.00),
(5, 10000.00),
(6, 4000.00),
(7, 6000.00),
(8, 2000.00),
(9, 12000.00),
(10, 8000.00);

-- Insert 10 rows of sample data into Loans table (user loans)
INSERT INTO Loans (UserID, LoanAmount, LoanType, IssuedDate, DueDate, Status) VALUES
(1, 10000.00, 'Home Loan', '2024-01-01', '2025-01-01', 'Active'),
(2, 5000.00, 'Car Loan', '2024-02-01', '2025-02-01', 'Active'),
(3, 2000.00, 'Personal Loan', '2024-03-01', '2025-03-01', 'Closed'),
(4, 3000.00, 'Home Loan', '2024-03-01', '2025-03-01', 'Active'),
(5, 15000.00, 'Business Loan', '2024-01-15', '2025-01-15', 'Active'),
(6, 10000.00, 'Car Loan', '2024-01-10', '2025-01-10', 'Active'),
(7, 5000.00, 'Home Loan', '2024-04-01', '2025-04-01', 'Closed'),
(8, 2500.00, 'Personal Loan', '2024-02-20', '2025-02-20', 'Active'),
(9, 12000.00, 'Car Loan', '2024-03-10', '2025-03-10', 'Closed'),
(10, 5000.00, 'Home Loan', '2024-05-01', '2025-05-01', 'Active');

-- Insert 10 rows of sample data into Investments table (user stock investments)
INSERT INTO Investments (UserID, StockSymbol, Shares, PurchasePrice, PurchaseDate) VALUES
(1, 'AAPL', 10, 150.00, '2024-01-01'),
(2, 'GOOG', 5, 1000.00, '2024-02-01'),
(3, 'TSLA', 20, 250.00, '2024-03-01'),
(4, 'AMZN', 15, 200.00, '2024-04-01'),
(5, 'MSFT', 8, 300.00, '2024-01-15'),
(6, 'TSLA', 25, 220.00, '2024-02-01'),
(7, 'GOOG', 10, 950.00, '2024-03-15'),
(8, 'AAPL', 12, 140.00, '2024-02-10'),
(9, 'MSFT', 6, 350.00, '2024-03-10'),
(10, 'AMZN', 5, 180.00, '2024-04-01');

-- Insert 10 rows of sample data into Donations table (user donations to bank)
INSERT INTO Donations (UserID, Amount, Note) VALUES
(1, 100.00, 'Donation to support community programs'),
(2, 50.00, 'Donation for charity event'),
(3, 200.00, 'Donation for disaster relief fund'),
(4, 150.00, 'Charity event sponsorship'),
(5, 250.00, 'Fundraising for children\'s education'),
(6, 300.00, 'Donation to animal shelter'),
(7, 120.00, 'Donation to health foundation'),
(8, 180.00, 'Donation for hospital construction'),
(9, 500.00, 'Donation for flood relief'),
(10, 100.00, 'Donation for environment preservation');

-- Insert 10 rows of sample data into BlockedAccounts table (user blocked accounts)
INSERT INTO BlockedAccounts (UserID, BlockReason, Status) VALUES
(1, 'Suspicious activity detected', 1),
(2, 'Account under investigation', 1),
(3, 'Fraudulent transaction attempt', 0),
(4, 'Non-compliance with bank policies', 1),
(5, 'Excessive failed login attempts', 0),
(6, 'Account frozen due to legal matter', 1),
(7, 'Suspicious login from unknown location', 0),
(8, 'Failed KYC verification', 1),
(9, 'Account flagged for suspicious transfers', 1),
(10, 'User requested account block', 0);


