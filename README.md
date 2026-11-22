# Python Expense Tracker and Budget Analyzer

## Project Overview

The **Python Expense Tracker and Budget Analyzer** is a personal finance management application developed using Python. It helps users record income and expenses, monitor spending habits, analyze monthly transactions, and manage their budgets.

The project includes both a **Python command-line application** and a **Flask-based web application** with a user-friendly interface.

This project was developed as part of the **Computational Thinking and Programming (2026CSAE100)** course at Bennett University.

## Objectives

- To develop a simple system for recording daily income and expenses.
- To store and manage financial transactions using CSV file handling.
- To calculate total income, total expenses, and remaining balance.
- To analyze monthly spending and category-wise expenses.
- To help users compare their spending against a monthly budget.
- To provide a user-friendly web interface for expense management.

## Features

1. **Add Transaction** – Record income and expenses with date, category, amount, and description.
2. **View Transactions** – Display all saved financial transactions.
3. **Monthly Analysis** – Calculate monthly income, expenses, and balance.
4. **Category Analysis** – Identify spending across different expense categories.
5. **Budget Analyzer** – Compare monthly expenses against a user-defined budget.
6. **Delete Transaction** – Remove an existing transaction.
7. **Export Report** – Generate a monthly financial report in TXT format.
8. **CSV Data Storage** – Store transactions locally using Python's CSV module.
9. **Web Dashboard** – Access the expense tracker through a Flask website.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| HTML | Website structure |
| CSS | Website styling |
| CSV | Transaction data storage |
| Git and GitHub | Version control and team collaboration |
| Visual Studio Code | Code editor |

## Project Structure

```text
Expense_Tracker_Project/
│
├── app.py
├── main.py
├── transactions.csv
├── monthly_report.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

## How to Run the Project

### Requirements

- Python 3 installed
- Flask installed
- Visual Studio Code or another code editor

### Run the Python Command-Line Application

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run:

```bash
python main.py
```

5. Follow the menu instructions displayed in the terminal.

### Run the Web Application

1. Open the project folder in VS Code.
2. Open the terminal.
3. Install Flask:

```bash
pip install flask
```

4. Start the Flask application:

```bash
python app.py
```

5. Open Google Chrome and visit:

```text
http://127.0.0.1:5000/
```

6. Use the website to add transactions, view summaries, analyze spending, and generate reports.

**Note:** The website runs locally on your computer. It is not currently deployed on a public hosting service.

## Python Concepts Used

- Variables and data types
- Conditional statements
- Loops
- Functions
- Lists and dictionaries
- File handling
- CSV operations
- Exception handling
- Modules and libraries

## Testing

The project is tested using sample income and expense transactions. Testing includes adding, viewing, deleting, and analyzing transactions, checking budget calculations, and exporting monthly reports.

## Future Improvements

- User login and authentication
- Graphical charts for expense analysis
- Database integration
- Online deployment
- Additional reporting and filtering options

## Team Contributions

This project was developed as a group assignment. Team members collaborate through GitHub by contributing code, testing, documentation, and project improvements.

| Team Member | Contribution |
|---|---|
| SAMRIDDHI JAIN | Menu design , input validation , calculations and report writing |
| PRANJALDEEP KAUR | CSV storage , loading , saving and transaction management |
| ASHU KUMAR GAUTAM | Monthly summaries , category analysis and budget comparison |
| ANSH VARDHAN RAO | Testing , screenshots , documentation and presentation |
| ANANT GUPTA | Report export , review or additional testing |


## Academic Information

**University:** Bennett University  
**Course:** Computational Thinking and Programming  
**Course Code:** 2026CSAE100  
**Project:** Python Expense Tracker and Budget Analyzer

## Conclusion

The Python Expense Tracker and Budget Analyzer demonstrates how Python programming, CSV file handling, and web development can be combined to create a practical personal finance management application.
