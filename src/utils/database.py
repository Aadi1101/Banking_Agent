import mysql.connector
from src.utils.config import get_config
from src.logger import logging

def db_connection():
    """Establishes and returns a MySQL database connection."""
    connection = mysql.connector.connect(
        host=get_config("DB_HOST"),
        user=get_config("DB_USER"),
        password=get_config("DB_PASSWORD"),
        database=get_config("DB_NAME"),
        port= get_config("DB_PORT")
    )

    if connection and connection.is_connected():
        return connection
    return None

def fetch_user_balance(user_id='1'):
    """Fetches the user's total balance from the Savings table."""
    logging.info("Entered Fetch user function")
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT balance FROM Savings WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        connection.close()
        logging.info("RESULT : ", result[0] if result else None)
        return str(result[0]) if result else "0"  # Return "0" if no balance found
    return "0"

def fetch_user_details(user_id='1'):
    """Fetches user details from the UserDetails table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT State, City, Pincode, Address FROM UserDetails WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result  # Returns a tuple or None
    return None

def fetch_user_transactions(user_id='1', limit=10):
    """Fetches user transactions from the Transactions table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT TransactionID, Amount, TransactionType, TransactionDate, Description FROM Transactions WHERE UserID = %s ORDER BY TransactionDate DESC LIMIT %s"
        cursor.execute(query, (user_id, limit))
        results = cursor.fetchall()
        connection.close()
        return results  # Returns a list of tuples or None
    return None

def fetch_user_savings(user_id='1'):
    """Fetches user savings balance from the Savings table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT Balance, LastUpdated FROM Savings WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result  # Returns a tuple or None
    return None

def fetch_user_loans(user_id='1'):
    """Fetches user loans from the Loans table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT LoanID, LoanAmount, LoanType, IssuedDate, DueDate, Status FROM Loans WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        connection.close()
        return results  # Returns a list of tuples or None
    return None

def fetch_user_investments(user_id='1'):
    """Fetches user investments from the Investments table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT InvestmentID, StockSymbol, Shares, PurchasePrice, PurchaseDate FROM Investments WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        connection.close()
        return results  # Returns a list of tuples or None
    return None

def fetch_user_donations(user_id='1'):
    """Fetches user donations from the Donations table."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT DonationID, Amount, DonationDate, Note FROM Donations WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        connection.close()
        return results  # Returns a list of tuples or None
    return None

def is_account_blocked(user_id='1'):
    """Checks if a user account is blocked."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT Status FROM BlockedAccounts WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        connection.close()
        return bool(result[0]) if result else False # Returns True if blocked, False otherwise.
    return False

def get_user_by_username(username):
    """Retrieves user details (ID and PasswordHash) by username."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT UserID, PasswordHash FROM Users WHERE Username = %s", (username,))
        user = cursor.fetchone()
        connection.close()
        return user  # Returns a tuple (UserID, PasswordHash) or None
    return None

def get_user_id_by_username(username):
    """Retrieves UserID by username."""
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE Username = %s", (username,))
        user_id = cursor.fetchone()
        connection.close()
        return user_id[0] if user_id else None  # Return UserID or None
    return None