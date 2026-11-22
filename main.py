
import csv
from datetime import datetime
from collections import defaultdict
from pathlib import Path

transactions = []
CSV_FILE = Path("transactions.csv")


def save_transactions():
    with open(CSV_FILE, "w", newline="") as file:
        fieldnames = ["id", "date", "type", "category", "amount", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)


def load_transactions():
    if not CSV_FILE.exists():
        return

    try:
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])
                transactions.append(row)

    except (ValueError, KeyError, OSError):
        print("Could not load transaction data. Please check transactions.csv.")


def main_menu():
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Monthly Summary")
    print("4. Category Analysis")
    print("5. Budget Analyzer")
    print("6. Delete Transaction")
    print("7. Export Report")
    print("8. Exit")


def add_transaction():
    print("\n===== ADD TRANSACTION =====")
    transaction_type = input("Enter type (Income/Expense): ").capitalize()

    if transaction_type not in ["Income", "Expense"]:
        print("Invalid transaction type!")
        return

    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
    except ValueError:
        print("Please enter a valid amount!")
        return

    description = input("Enter description: ")

    try:
        date = input("Enter date (DD-MM-YYYY): ")
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format!")
        return

    new_id = max([t["id"] for t in transactions], default=0) + 1

    transaction = {
        "id": new_id,
        "date": date,
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description
    }

    transactions.append(transaction)
    save_transactions()
    print("Transaction added and saved successfully!")


def view_transactions():
    print("\n===== ALL TRANSACTIONS =====")

    if not transactions:
        print("No transactions found!")
        return

    sorted_transactions = sorted(
        transactions,
        key=lambda x: datetime.strptime(x["date"], "%d-%m-%Y")
    )

    for transaction in sorted_transactions:
        print("\nID:", transaction["id"])
        print("Date:", transaction["date"])
        print("Type:", transaction["type"])
        print("Category:", transaction["category"])
        print("Amount: Rs.", transaction["amount"])
        print("Description:", transaction["description"])


def monthly_summary():
    print("\n===== MONTHLY SUMMARY =====")
    month = input("Enter month (MM-YYYY): ")

    try:
        datetime.strptime(month, "%m-%Y")
    except ValueError:
        print("Invalid month format!")
        return

    total_income = 0
    total_expenses = 0
    count = 0

    for transaction in transactions:
        transaction_month = datetime.strptime(
            transaction["date"], "%d-%m-%Y"
        ).strftime("%m-%Y")

        if transaction_month == month:
            count += 1

            if transaction["type"] == "Income":
                total_income += transaction["amount"]
            else:
                total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    print("\nMonth:", month)
    print("Total Income: Rs.", total_income)
    print("Total Expenses: Rs.", total_expenses)
    print("Remaining Balance: Rs.", balance)
    print("Total Transactions:", count)


def category_analysis():
    print("\n===== CATEGORY ANALYSIS =====")
    category_totals = defaultdict(float)

    for transaction in transactions:
        if transaction["type"] == "Expense":
            category_totals[transaction["category"]] += transaction["amount"]

    if not category_totals:
        print("No expense transactions found!")
        return

    for category, total in category_totals.items():
        print(category, ": Rs.", total)

    highest_category = max(category_totals, key=category_totals.get)

    print("\nHighest Spending Category:", highest_category)
    print("Highest Spending Amount: Rs.", category_totals[highest_category])


def budget_analyzer():
    print("\n===== BUDGET ANALYZER =====")
    month = input("Enter month (MM-YYYY): ")

    try:
        datetime.strptime(month, "%m-%Y")
        budget = float(input("Enter your monthly budget: "))

        if budget <= 0:
            print("Budget must be greater than zero!")
            return

    except ValueError:
        print("Invalid input! Please enter a valid month and budget.")
        return

    total_expenses = 0

    for transaction in transactions:
        transaction_month = datetime.strptime(
            transaction["date"], "%d-%m-%Y"
        ).strftime("%m-%Y")

        if transaction_month == month and transaction["type"] == "Expense":
            total_expenses += transaction["amount"]

    remaining_budget = budget - total_expenses

    print("\nMonth:", month)
    print("Monthly Budget: Rs.", budget)
    print("Total Expenses: Rs.", total_expenses)

    if remaining_budget > 0:
        print("Remaining Budget: Rs.", remaining_budget)
        print("Status: You are within your budget!")

    elif remaining_budget == 0:
        print("Remaining Budget: Rs. 0")
        print("Status: You have used your entire budget!")

    else:
        print("Budget Exceeded By: Rs.", abs(remaining_budget))
        print("Status: WARNING! You have exceeded your budget!")


def delete_transaction():
    print("\n===== DELETE TRANSACTION =====")

    if not transactions:
        print("No transactions available to delete!")
        return

    view_transactions()

    try:
        transaction_id = int(input("\nEnter transaction ID to delete: "))
    except ValueError:
        print("Please enter a valid ID!")
        return

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            confirm = input(
                "Are you sure you want to delete? (yes/no): "
            ).lower()

            if confirm == "yes":
                transactions.remove(transaction)
                save_transactions()
                print("Transaction deleted successfully!")
            else:
                print("Deletion cancelled!")

            return

    print("Transaction ID not found!")


def export_report():
    print("\n===== EXPORT MONTHLY REPORT =====")
    month = input("Enter month (MM-YYYY): ")

    try:
        datetime.strptime(month, "%m-%Y")
    except ValueError:
        print("Invalid month format!")
        return

    monthly_transactions = []
    category_totals = defaultdict(float)
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        transaction_month = datetime.strptime(
            transaction["date"], "%d-%m-%Y"
        ).strftime("%m-%Y")

        if transaction_month == month:
            monthly_transactions.append(transaction)

            if transaction["type"] == "Income":
                total_income += transaction["amount"]
            else:
                total_expenses += transaction["amount"]
                category_totals[transaction["category"]] += transaction["amount"]

    balance = total_income - total_expenses

    try:
        with open("monthly_report.txt", "w") as file:
            file.write("===== MONTHLY EXPENSE REPORT =====\n")
            file.write("Month: " + month + "\n\n")

            file.write("Total Income: Rs. " + str(total_income) + "\n")
            file.write("Total Expenses: Rs. " + str(total_expenses) + "\n")
            file.write("Remaining Balance: Rs. " + str(balance) + "\n")
            file.write(
                "Total Transactions: " + str(len(monthly_transactions)) + "\n"
            )

            file.write("\n===== CATEGORY-WISE EXPENSES =====\n")

            if category_totals:
                for category, total in category_totals.items():
                    file.write(category + ": Rs. " + str(total) + "\n")
            else:
                file.write("No expense transactions found.\n")

            file.write("\n===== TRANSACTION DETAILS =====\n")

            if monthly_transactions:
                for transaction in monthly_transactions:
                    file.write(
                        "\nID: " + str(transaction["id"])
                        + "\nDate: " + transaction["date"]
                        + "\nType: " + transaction["type"]
                        + "\nCategory: " + transaction["category"]
                        + "\nAmount: Rs. " + str(transaction["amount"])
                        + "\nDescription: " + transaction["description"]
                        + "\n"
                    )
            else:
                file.write("No transactions found for this month.\n")

        print("Monthly report exported successfully!")
        print("Open monthly_report.txt to view your report.")

    except OSError:
        print("Could not create the report file!")


load_transactions()

while True:
    main_menu()
    choice = input("Enter your choice (1-8): ")

    if choice == "1":
        add_transaction()
    elif choice == "2":
        view_transactions()
    elif choice == "3":
        monthly_summary()
    elif choice == "4":
        category_analysis()
    elif choice == "5":
        budget_analyzer()
    elif choice == "6":
        delete_transaction()
    elif choice == "7":
        export_report()
    elif choice == "8":
        print("Thank you for using Expense Tracker!")
        break
    else:
        print("Invalid choice! Please try again.")
