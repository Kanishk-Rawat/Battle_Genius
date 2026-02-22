
import csv
import os
import random

# --- Configuration ---
DATA_FILE = 'accounts.csv'
FIELDNAMES = ['Account_Number', 'Name', 'Type', 'Balance', 'Contact']
# ---------------------

# --- Helper Functions for File/Data Management ---

def initialize_file():
    """Checks if the CSV file exists. If not, creates it with headers."""
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
            print(f"✅ Data file '{DATA_FILE}' created successfully.")
        except IOError as e:
            print(f"❌ Error creating file: {e}")

def load_data():
    """Loads all account records from the CSV file."""
    initialize_file()
    try:
        with open(DATA_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=FIELDNAMES)
            data = list(reader)
            # Skip the header row if it exists
            if data and data[0].get('Account_Number') == 'Account_Number':
                return data[1:]
            return data
    except Exception as e:
        print(f"❌ An error occurred while loading data: {e}")
        return []

def save_data(data):
    """Writes the entire list of account records back to the CSV file."""
    try:
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(data)
        return True
    except IOError as e:
        print(f"❌ Error saving data: {e}")
        return False

def find_account_by_number(data, acc_no):
    """Helper to search for an account by Account Number."""
    for account in data:
        if account.get('Account_Number') == acc_no:
            return account
    return None

def generate_account_number(data):
    """Generates a unique 6-digit account number."""
    existing_numbers = {acc['Account_Number'] for acc in data}
    while True:
        # Generate a 6-digit number as a string
        new_acc_no = str(random.randint(100000, 999999))
        if new_acc_no not in existing_numbers:
            return new_acc_no

# --- Core Banking Management Functions ---

def create_account():
    """Prompts user for details to open a new bank account."""
    print("\n--- CREATE NEW ACCOUNT ---")
    data = load_data()

    acc_no = generate_account_number(data)
    name = input("Enter Account Holder Name: ").strip()

    while True:
        acc_type = input("Enter Account Type (Savings/Current): ").strip().title()
        if acc_type in ['Savings', 'Current']:
            break
        print("Invalid account type. Must be 'Savings' or 'Current'.")

    while True:
        try:
            balance = float(input("Enter Initial Deposit (Minimum ₹1000): "))
            if balance < 1000:
                print("Initial deposit must be at least ₹1000.")
                continue
            break
        except ValueError:
            print("Invalid input for balance. Please enter a number.")

    contact = input("Enter Contact Number: ").strip()

    new_account = {
        'Account_Number': acc_no,
        'Name': name,
        'Type': acc_type,
        'Balance': f"{balance:.2f}", # Store balance with two decimal places
        'Contact': contact
    }

    data.append(new_account)
    if save_data(data):
        print(f"\n✅ Account created successfully!")
        print(f"   Account Number: {acc_no}")
        print(f"   Name: {name}")

    # --- MySQL/Binary Logic Swap ---
    # * MySQL: Execute INSERT query with values.
    # * Binary: Append dict to list, then pickle.dump().
    # -------------------------------

def deposit_money():
    """Allows a user to deposit money into an existing account."""
    print("\n--- DEPOSIT MONEY ---")
    acc_no = input("Enter Account Number: ").strip()
    data = load_data()
    account = find_account_by_number(data, acc_no)

    if account:
        print(f"Account Holder: {account['Name']}")
        print(f"Current Balance: ₹{account['Balance']}")

        while True:
            try:
                amount = float(input("Enter amount to deposit (Min ₹100): "))
                if amount < 100:
                    print("Deposit amount must be ₹100 or more.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

        # Update balance
        new_balance = float(account['Balance']) + amount
        account['Balance'] = f"{new_balance:.2f}"

        if save_data(data):
            print(f"✅ ₹{amount:.2f} deposited successfully.")
            print(f"   New Balance: ₹{new_balance:.2f}")
    else:
        print(f"❌ Account {acc_no} not found.")

    # --- MySQL/Binary Logic Swap ---
    # * MySQL: SELECT balance, calculate new balance, then execute UPDATE query.
    # * Binary: Update dict in list, then pickle.dump().
    # -------------------------------

def withdraw_money():
    """Allows a user to withdraw money from an existing account."""
    print("\n--- WITHDRAW MONEY ---")
    acc_no = input("Enter Account Number: ").strip()
    data = load_data()
    account = find_account_by_number(data, acc_no)

    if account:
        print(f"Account Holder: {account['Name']}")
        current_balance = float(account['Balance'])
        print(f"Current Balance: ₹{current_balance:.2f}")

        while True:
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount > current_balance:
                    print("❌ Insufficient balance.")
                    continue
                if amount <= 0:
                    print("Withdrawal amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

        # Update balance
        new_balance = current_balance - amount
        account['Balance'] = f"{new_balance:.2f}"

        if save_data(data):
            print(f"✅ ₹{amount:.2f} withdrawn successfully.")
            print(f"   Remaining Balance: ₹{new_balance:.2f}")
    else:
        print(f"❌ Account {acc_no} not found.")

    # --- MySQL/Binary Logic Swap ---
    # * MySQL: Check balance, then execute UPDATE query.
    # * Binary: Update dict in list, then pickle.dump().
    # -------------------------------

def check_balance():
    """Displays the balance of a specific account."""
    print("\n--- CHECK BALANCE ---")
    acc_no = input("Enter Account Number: ").strip()
    data = load_data()
    account = find_account_by_number(data, acc_no)

    if account:
        print(f"\n💰 Account Holder: {account['Name']}")
        print(f"   Account Number: {account['Account_Number']}")
        print(f"   Account Type:   {account['Type']}")
        print(f"   Current Balance: ₹{account['Balance']}")
    else:
        print(f"❌ Account {acc_no} not found.")

    # --- MySQL/Binary Logic Swap ---
    # * MySQL: Execute a SELECT query for the specific account number.
    # * Binary: Same as CSV, use find_account_by_number.
    # -------------------------------

def view_all_accounts():
    """Displays all account records in a formatted table."""
    print("\n--- ALL BANK ACCOUNTS ---")
    data = load_data()

    if not data:
        print("💡 No accounts found.")
        return

    # Define table header format
    header = "{:<12} {:<25} {:<10} {:<15} {:<15}".format(
        "ACC NO", "NAME", "TYPE", "BALANCE (₹)", "CONTACT"
    )
    print("=" * len(header))
    print(header)
    print("=" * len(header))

    # Print Data Rows
    for account in data:
        print("{:<12} {:<25} {:<10} {:<15} {:<15}".format(
            account.get('Account_Number', 'N/A'),
            account.get('Name', 'N/A'),
            account.get('Type', 'N/A'),
            account.get('Balance', 'N/A'),
            account.get('Contact', 'N/A')
        ))
    print("-" * len(header))

# --- Main Application Loop ---

def main_menu():
    """Displays the main menu and handles user input for navigation."""

    initialize_file()

    while True:
        print("\n\n=== BANKING MANAGEMENT SYSTEM ===")
        print("1. Create New Account 👤")
        print("2. Deposit Money ⬆️")
        print("3. Withdraw Money ⬇️")
        print("4. Check Balance 🔍")
        print("5. View All Accounts 📜")
        print("6. Exit 🚪")
        print("---------------------------------")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            view_all_accounts()
        elif choice == '6':
            print("\n👋 Thank you for using the Banking Management System. Goodbye!")
            break
        else:
            print("❗ Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress ENTER to return to the main menu...")

# --- Run the Program ---
if __name__ == "__main__":
    main_menu()

