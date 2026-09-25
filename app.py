import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Banking System", page_icon="🏦")

# Store accounts during the current app session
if "accounts" not in st.session_state:
    st.session_state.accounts = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = None


def generate_account_number():
    while True:
        number = str(random.randint(10000000, 99999999))
        if number not in st.session_state.accounts:
            return number


def add_transaction(account, transaction):
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    account["transactions"].append(f"{time} - {transaction}")


st.title("🏦 Banking System")
st.write("A simple Python Banking System")

# ---------------- CREATE ACCOUNT ----------------

st.header("Create Account")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
pin = st.text_input("Create 4-digit PIN", type="password")

if st.button("Create Account"):
    if not name or not phone:
        st.error("Please enter name and phone number.")
    elif len(pin) != 4 or not pin.isdigit():
        st.error("PIN must contain exactly 4 digits.")
    else:
        account_number = generate_account_number()

        st.session_state.accounts[account_number] = {
            "name": name,
            "phone": phone,
            "pin": pin,
            "balance": 0.0,
            "transactions": []
        }

        st.success("Account created successfully!")
        st.info(f"Your Account Number is: {account_number}")


# ---------------- LOGIN ----------------

st.header("Login")

account_number = st.text_input("Account Number")
login_pin = st.text_input("PIN", type="password")

if st.button("Login"):
    if account_number in st.session_state.accounts:
        account = st.session_state.accounts[account_number]

        if account["pin"] == login_pin:
            st.session_state.logged_in = account_number
            st.success("Login successful!")
        else:
            st.error("Incorrect PIN.")
    else:
        st.error("Account not found.")


# ---------------- ACCOUNT MENU ----------------

if st.session_state.logged_in:

    account_number = st.session_state.logged_in
    account = st.session_state.accounts[account_number]

    st.divider()
    st.header(f"Welcome, {account['name']}")

    st.metric("Current Balance", f"₹{account['balance']:.2f}")

    # Deposit
    st.subheader("Deposit")

    deposit_amount = st.number_input(
        "Deposit Amount",
        min_value=0.0,
        step=100.0,
        key="deposit"
    )

    if st.button("Deposit Money"):
        if deposit_amount > 0:
            account["balance"] += deposit_amount
            add_transaction(
                account,
                f"Deposited ₹{deposit_amount:.2f}"
            )
            st.success("Amount deposited successfully!")
            st.rerun()
        else:
            st.error("Enter a valid amount.")

    # Withdraw
    st.subheader("Withdraw")

    withdraw_amount = st.number_input(
        "Withdrawal Amount",
        min_value=0.0,
        step=100.0,
        key="withdraw"
    )

    if st.button("Withdraw Money"):
        if withdraw_amount <= 0:
            st.error("Enter a valid amount.")
        elif withdraw_amount > account["balance"]:
            st.error("Insufficient balance.")
        else:
            account["balance"] -= withdraw_amount
            add_transaction(
                account,
                f"Withdrawn ₹{withdraw_amount:.2f}"
            )
            st.success("Amount withdrawn successfully!")
            st.rerun()

    # Transaction History
    st.subheader("Transaction History")

    if account["transactions"]:
        for transaction in account["transactions"]:
            st.write("•", transaction)
    else:
        st.info("No transactions found.")

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = None
        st.rerun()