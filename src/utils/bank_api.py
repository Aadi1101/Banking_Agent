from src.utils.database import fetch_user_balance, fetch_user_details, fetch_user_transactions, fetch_user_savings, fetch_user_loans, fetch_user_investments, fetch_user_donations, is_account_blocked
import streamlit as st
from src.logger import logging

class BankAPI:
    def __init__(self):
        self.user_id = '1'
        logging.info("USER ID: ", self.user_id)

    def check_balance(self, query):
        """Checks the user's balance using the database function."""
        self.user_id = str(st.session_state['user_id'])
        logging.info("USERID - ", self.user_id)
        balance = fetch_user_balance(self.user_id)
        logging.info("BALANCE: ", balance)
        return balance if balance is not None else "Error fetching balance."

    def get_user_details(self, user_id):
        """Retrieves user details."""
        self.user_id = str(st.session_state['user_id'])
        details = fetch_user_details(self.user_id)
        if details:
            return {
                "state": details[0],
                "city": details[1],
                "pincode": details[2],
                "address": details[3]
            }
        return "User details not found."

    def get_transactions(self, user_id, limit=10):
        """Retrieves user transactions."""
        self.user_id = str(st.session_state['user_id'])
        transactions = fetch_user_transactions(self.user_id, limit)
        if transactions:
            return [
                {
                    "transaction_id": transaction[0],
                    "amount": transaction[1],
                    "type": transaction[2],
                    "date": transaction[3],
                    "description": transaction[4]
                }
                for transaction in transactions
            ]
        return "No transactions found."

    def get_savings_balance(self, user_id):
        """Retrieves user savings balance."""
        self.user_id = str(st.session_state['user_id'])
        savings = fetch_user_savings(self.user_id)
        if savings:
            return {"balance": savings[0], "last_updated": savings[1]}
        return "Savings information not found."

    def get_loans(self, user_id):
        """Retrieves user loans."""
        self.user_id = str(st.session_state['user_id'])
        loans = fetch_user_loans(self.user_id)
        if loans:
            return str([
                {
                    "loan_id": loan[0],
                    "amount": loan[1],
                    "type": loan[2],
                    "issued_date": loan[3],
                    "due_date": loan[4],
                    "status": loan[5]
                }
                for loan in loans
            ])
        return "No loans found."

    def get_investments(self, user_id):
        """Retrieves user investments."""
        self.user_id = str(st.session_state['user_id'])
        investments = fetch_user_investments(self.user_id)
        if investments:
            return str([
                {
                    "investment_id": investment[0],
                    "stock_symbol": investment[1],
                    "shares": investment[2],
                    "purchase_price": investment[3],
                    "purchase_date": investment[4]
                }
                for investment in investments
            ])
        return "No investments found."

    def get_donations(self, user_id):
        """Retrieves user donations."""
        self.user_id = str(st.session_state['user_id'])
        donations = fetch_user_donations(self.user_id)
        if donations:
            return str([
                {
                    "donation_id": donation[0],
                    "amount": donation[1],
                    "date": donation[2],
                    "note": donation[3]
                }
                for donation in donations
            ])
        return "No donations found."

    def is_blocked(self, user_id):
        """Checks if a user account is blocked."""
        self.user_id = str(st.session_state['user_id'])
        return is_account_blocked(self.user_id)