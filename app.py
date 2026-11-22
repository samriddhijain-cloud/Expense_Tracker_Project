
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import csv
import math

app = Flask(__name__)
app.secret_key = "expense-tracker-local-project"

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "transactions.csv"
REPORT_FILE = BASE_DIR / "monthly_report.txt"

FIELDS = ["id", "date", "type", "category", "amount", "description"]


def load_transactions():
    transactions = []

    if not CSV_FILE.exists():
        return transactions

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])

                datetime.strptime(row["date"], "%d-%m-%Y")

                transactions.append(row)

    except (ValueError, KeyError, OSError, TypeError):
        flash("Some transaction data could not be loaded.", "error")

    return transactions


def save_transactions(transactions):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)


def get_month(transaction):
    return datetime.strptime(
        transaction["date"], "%d-%m-%Y"
    ).strftime("%m-%Y")


def calculate_summary(transactions):
    income = 0
    expenses = 0

    for transaction in transactions:
        if transaction["type"] == "Income":
            income += transaction["amount"]
        elif transaction["type"] == "Expense":
            expenses += transaction["amount"]

    return income, expenses, income - expenses


@app.route("/")
def home():
    transactions = load_transactions()

    transactions.sort(
        key=lambda t: datetime.strptime(t["date"], "%d-%m-%Y"),
        reverse=True
    )

    total_income, total_expenses, balance = calculate_summary(transactions)

    selected_month = request.args.get(
        "month", datetime.now().strftime("%Y-%m")
    )

    try:
        month = datetime.strptime(selected_month, "%Y-%m").strftime("%m-%Y")
    except ValueError:
        selected_month = datetime.now().strftime("%Y-%m")
        month = datetime.now().strftime("%m-%Y")

    monthly_transactions = [
        t for t in transactions if get_month(t) == month
    ]

    monthly_income, monthly_expenses, monthly_balance = calculate_summary(
        monthly_transactions
    )

    category_totals = defaultdict(float)

    for transaction in monthly_transactions:
        if transaction["type"] == "Expense":
            category_totals[transaction["category"]] += transaction["amount"]

    highest_category = (
        max(category_totals, key=category_totals.get)
        if category_totals else "None"
    )

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        selected_month=selected_month,
        month=month,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_balance=monthly_balance,
        monthly_count=len(monthly_transactions),
        category_totals=dict(category_totals),
        highest_category=highest_category
    )


@app.route("/add", methods=["POST"])
def add_transaction():
    transactions = load_transactions()

    transaction_type = request.form.get("type", "").capitalize()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    date = request.form.get("date", "")

    try:
        amount = float(request.form.get("amount", ""))
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        flash("Please enter a valid amount and date.", "error")
        return redirect(url_for("home"))

    if (
        transaction_type not in ["Income", "Expense"]
        or not category
        or amount <= 0
        or not math.isfinite(amount)
    ):
        flash("Please enter valid transaction details.", "error")
        return redirect(url_for("home"))

    new_id = max([t["id"] for t in transactions], default=0) + 1

    transactions.append({
        "id": new_id,
        "date": parsed_date.strftime("%d-%m-%Y"),
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description
    })

    save_transactions(transactions)
    flash("Transaction added successfully!", "success")

    return redirect(url_for("home"))


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    transactions = load_transactions()

    updated = [
        t for t in transactions if t["id"] != transaction_id
    ]

    if len(updated) == len(transactions):
        flash("Transaction not found.", "error")
    else:
        save_transactions(updated)
        flash("Transaction deleted successfully!", "success")

    return redirect(url_for("home"))


@app.route("/budget", methods=["POST"])
def budget_analyzer():
    selected_month = request.form.get("month", "")
    budget_text = request.form.get("budget", "")

    try:
        month = datetime.strptime(
            selected_month, "%Y-%m"
        ).strftime("%m-%Y")

        budget = float(budget_text)

        if budget <= 0 or not math.isfinite(budget):
            raise ValueError

    except ValueError:
        flash("Enter a valid month and positive budget.", "error")
        return redirect(url_for("home"))

    transactions = load_transactions()

    monthly_expenses = sum(
        t["amount"]
        for t in transactions
        if get_month(t) == month and t["type"] == "Expense"
    )

    remaining = budget - monthly_expenses

    if remaining > 0:
        message = f"You are within budget! Remaining: Rs. {remaining:.2f}"
        status = "success"
    elif remaining == 0:
        message = "You have used your entire monthly budget!"
        status = "warning"
    else:
        message = f"Budget exceeded by Rs. {abs(remaining):.2f}!"
        status = "error"

    flash(
        f"Budget: Rs. {budget:.2f} | "
        f"Expenses: Rs. {monthly_expenses:.2f} | {message}",
        status
    )

    return redirect(url_for("home", month=selected_month))


@app.route("/export")
def export_report():
    selected_month = request.args.get("month", "")

    try:
        month = datetime.strptime(
            selected_month, "%Y-%m"
        ).strftime("%m-%Y")
    except ValueError:
        flash("Please select a valid month.", "error")
        return redirect(url_for("home"))

    transactions = load_transactions()

    monthly_transactions = [
        t for t in transactions if get_month(t) == month
    ]

    income, expenses, balance = calculate_summary(monthly_transactions)

    categories = defaultdict(float)

    for transaction in monthly_transactions:
        if transaction["type"] == "Expense":
            categories[transaction["category"]] += transaction["amount"]

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write("===== MONTHLY EXPENSE REPORT =====\n")
            file.write(f"Month: {month}\n\n")
            file.write(f"Total Income: Rs. {income:.2f}\n")
            file.write(f"Total Expenses: Rs. {expenses:.2f}\n")
            file.write(f"Remaining Balance: Rs. {balance:.2f}\n")
            file.write(f"Total Transactions: {len(monthly_transactions)}\n")

            file.write("\n===== CATEGORY-WISE EXPENSES =====\n")

            if categories:
                for category, total in categories.items():
                    file.write(f"{category}: Rs. {total:.2f}\n")
            else:
                file.write("No expense transactions found.\n")

            file.write("\n===== TRANSACTION DETAILS =====\n")

            if monthly_transactions:
                for t in monthly_transactions:
                    file.write(
                        f"\nID: {t['id']}\n"
                        f"Date: {t['date']}\n"
                        f"Type: {t['type']}\n"
                        f"Category: {t['category']}\n"
                        f"Amount: Rs. {t['amount']:.2f}\n"
                        f"Description: {t['description']}\n"
                    )
            else:
                file.write("No transactions found for this month.\n")

    except OSError:
        flash("Could not create the report file.", "error")
        return redirect(url_for("home"))

    return send_file(
        REPORT_FILE,
        as_attachment=True,
        download_name=f"expense_report_{month}.txt"
    )


if __name__ == "__main__":
    app.run(debug=True)
