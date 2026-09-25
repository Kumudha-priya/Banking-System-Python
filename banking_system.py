import random
from datetime import datetime

accounts = {}


def generate_account_number():
    while True:
        account_number = str(random.randint(10000000, 99999999))
        if account_number not in accounts:
            return account_number


def add_transaction(account, transaction):
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    account["transactions"].append(f"{time} - {transaction}")


def create_account():
    print("\n===== CREATE ACCOUNT =====")

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")

    while True:
        pin = input("Create a 4-digit PIN: ")

        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("PIN must contain exactly 4 digits.")

    account_number = generate_account_number()

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)
    print("Please remember your account number and PIN.")


def login():
    print("\n===== LOGIN =====")

    account_number = input("Enter account number: ")
    pin = input("Enter PIN: ")

    if account_number in accounts:
        if accounts[account_number]["pin"] == pin:
            print("\nLogin successful!")
            account_menu(account_number)
        else:
            print("Incorrect PIN.")
    else:
        print("Account not found.")


def check_balance(account):
    print("\n===== ACCOUNT BALANCE =====")
    print("Current Balance: ₹", account["balance"])


def deposit(account):
    print("\n===== DEPOSIT MONEY =====")

    try:
        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            print("Enter a valid amount.")
            return

        account["balance"] += amount

        add_transaction(account, f"Deposited ₹{amount:.2f}")

        print("Amount deposited successfully.")
        print("New Balance: ₹", account["balance"])

    except ValueError:
        print("Please enter a valid number.")


def withdraw(account):
    print("\n===== WITHDRAW MONEY =====")

    try:
        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            print("Enter a valid amount.")
            return

        if amount > account["balance"]:
            print("Insufficient balance.")
            return

        account["balance"] -= amount

        add_transaction(account, f"Withdrawn ₹{amount:.2f}")

        print("Amount withdrawn successfully.")
        print("Remaining Balance: ₹", account["balance"])

    except ValueError:
        print("Please enter a valid number.")


def transfer(sender_account_number):
    print("\n===== TRANSFER MONEY =====")

    receiver_account_number = input("Enter receiver account number: ")

    if receiver_account_number not in accounts:
        print("Receiver account not found.")
        return

    if receiver_account_number == sender_account_number:
        print("You cannot transfer money to the same account.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))

        if amount <= 0:
            print("Enter a valid amount.")
            return

        sender = accounts[sender_account_number]
        receiver = accounts[receiver_account_number]

        if amount > sender["balance"]:
            print("Insufficient balance.")
            return

        sender["balance"] -= amount
        receiver["balance"] += amount

        add_transaction(
            sender,
            f"Transferred ₹{amount:.2f} to Account {receiver_account_number}"
        )

        add_transaction(
            receiver,
            f"Received ₹{amount:.2f} from Account {sender_account_number}"
        )

        print("Transfer successful.")
        print("Remaining Balance: ₹", sender["balance"])

    except ValueError:
        print("Please enter a valid number.")


def transaction_history(account):
    print("\n===== TRANSACTION HISTORY =====")

    if len(account["transactions"]) == 0:
        print("No transactions found.")
    else:
        for transaction in account["transactions"]:
            print(transaction)


def change_pin(account):
    print("\n===== CHANGE PIN =====")

    old_pin = input("Enter old PIN: ")

    if old_pin != account["pin"]:
        print("Incorrect old PIN.")
        return

    while True:
        new_pin = input("Enter new 4-digit PIN: ")
        confirm_pin = input("Confirm new PIN: ")

        if len(new_pin) != 4 or not new_pin.isdigit():
            print("PIN must contain exactly 4 digits.")
            continue

        if new_pin != confirm_pin:
            print("PINs do not match.")
            continue

        break

    account["pin"] = new_pin

    add_transaction(account, "PIN changed")

    print("PIN changed successfully.")


def account_menu(account_number):
    account = accounts[account_number]

    while True:
        print("\n==============================")
        print("        ACCOUNT MENU")
        print("==============================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance(account)

        elif choice == "2":
            deposit(account)

        elif choice == "3":
            withdraw(account)

        elif choice == "4":
            transfer(account_number)

        elif choice == "5":
            transaction_history(account)

        elif choice == "6":
            change_pin(account)

        elif choice == "7":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    while True:
        print("\n==============================")
        print("       BANKING SYSTEM")
        print("==============================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Thank you for using Banking System.")
            break

        else:
            print("Invalid choice. Please try again.")


main()