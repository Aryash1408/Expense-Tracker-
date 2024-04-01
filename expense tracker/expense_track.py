from expenses import Expense
import calendar
import datetime
import mysql.connector
from mysql.connector import Error

# Function to connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='expense_connector_db',
            user='root',
            password='password'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to save expense to database
def save_expense_to_database(expense, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO expenses (name, category, amount) VALUES (%s, %s, %s)",
                       (expense.name, expense.category, expense.amount))
        connection.commit()
        print("Expense saved to database successfully")
    except Error as e:
        print(f"Error saving expense to database: {e}")

# Function to close database connection
def close_database_connection(connection):
    if connection.is_connected():
        connection.close()
        print('Database connection closed')

def main():
    print("Running Expense Tracker!")
    budget = 3000

    connection = connect_to_database()

    # Get user input for expense 
    expense = user_input_expense()

    # Save expense to database
    if connection:
        save_expense_to_database(expense, connection)

    # Summarize expenses
    if connection:
        summarizing_expense(connection, budget)

    # Close database connection
    if connection:
        close_database_connection(connection)

def user_input_expense():
    print("Getting User Input for Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_category = [
        "🍔Food",
        "🏡Rent",
        "💻Work",
        "🚤Travelling",
        "😈Misc"
    ]
    
    while True:
        print("Select the categories")
        # give index as well as name of category from the list
        for i, category_name in enumerate(expense_category): 
            print(f" {i+1}. {category_name}")

        value_range = f"[1-{len(expense_category)}]"
        selected_choice = int(input(f"\nPlease enter your choice (press {value_range}) :")) - 1 #because we added 1 to index but it start with 0 in list

        if selected_choice in range(len(expense_category)):
            selected_category = expense_category[selected_choice]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else: 
            print("please enter a valid choice")

def summarizing_expense(connection, budget):
    print("Summarizing User Expenses")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        amount_by_category = {}
        for expense in expenses:
            key = expense[1]
            if key in amount_by_category:
                amount_by_category[key] += expense[3]
            else:
                amount_by_category[key] = expense[3]
    
        print("Expenses by Category")
        for key, amount in amount_by_category.items():
            print(f"  {key} : Rs{amount}")
        
        total_spent = sum([x[3] for x in expenses])
        print(f"You've spent {total_spent} this month!")

        remaining_budget = budget - total_spent
        if remaining_budget < 0:
            print(f"\nYour budget is over! You've overspent by Rs {-remaining_budget}.\nPlease try reducing your spending.")
        else:
            print(f"Budget Remaining : RS{remaining_budget}")

        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        daily_budget = remaining_budget / remaining_days
        print(green(f"👉 Budget Per Day: Rs{daily_budget:.2f}"))
    except Error as e:
        print(f"Error summarizing expenses: {e}")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__=='__main__':
    main()
