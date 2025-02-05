import os
import platform
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "6qbd*****6",
    "database": "food"
}


def get_db_connection():
    """Establishes and returns database connection and cursor"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        return conn, cursor
    except Error as e:
        print(f"Database connection error: {e}")
        exit()


def close_db_connection(conn, cursor):
    """Closes database connection"""
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except Error as e:
        print(f"Error closing connection: {e}")


def get_valid_input(prompt, input_type=str):
    """Validates user input based on type"""
    while True:
        try:
            user_input = input_type(input(prompt))
            if input_type == str and not user_input:
                raise ValueError("Input cannot be empty")
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def handle_database_operation(query, params=None, fetch=False):
    """Handles database operations with error handling"""
    conn, cursor = get_db_connection()
    try:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        print("Operation completed successfully.")
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        close_db_connection(conn, cursor)


def add_customer():
    """Adds a new customer to the database"""
    print("\n--- Add New Customer ---")
    fields = [
        ("Customer ID", int),
        ("Customer Name", str),
        ("Phone Number", int),
        ("Payment Method (1=Credit Card, 2=Debit Card)", int),
        ("Payment Status (Paid/Unpaid)", str),
        ("Email", str),
        ("Order ID", int),
        ("Date (YYYY-MM-DD)", str)
    ]

    values = [get_valid_input(f"Enter {field[0]}: ", field[1]) for field in fields]

    query = """INSERT INTO customer 
               (c_id, name, cphone, payment, pstatus, email, orderid, date) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    handle_database_operation(query, tuple(values))


def add_employee():
    """Adds a new employee to the database"""
    print("\n--- Add New Employee ---")
    fields = [
        ("Employee ID", int),
        ("Employee Name", str),
        ("Gender", str),
        ("Age", int),
        ("Phone Number", int),
        ("Password", str)
    ]

    values = [get_valid_input(f"Enter {field[0]}: ", field[1]) for field in fields]

    query = """INSERT INTO Employee 
               (Emp_id, ename, emp_g, eage, emp_phone, pwd) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    handle_database_operation(query, tuple(values))


def add_food_item():
    """Adds a new food item to the database"""
    print("\n--- Add New Food Item ---")
    fields = [
        ("Food ID", int),
        ("Food Name", str),
        ("Food Size", str),
        ("Price", int)
    ]

    values = [get_valid_input(f"Enter {field[0]}: ", field[1]) for field in fields]

    query = """INSERT INTO Food 
               (Food_id, Foodname, Food_size, prize) 
               VALUES (%s, %s, %s, %s)"""
    handle_database_operation(query, tuple(values))


def add_order():
    """Adds a new food order to the database"""
    print("\n--- Add New Order ---")
    fields = [
        ("Order ID", int),
        ("Customer ID", int),
        ("Employee ID", int),
        ("Food ID", int),
        ("Quantity", int),
        ("Total Price", int)
    ]

    values = [get_valid_input(f"Enter {field[0]}: ", field[1]) for field in fields]

    query = """INSERT INTO OrderFood 
               (OrderF_id, C_id, Emp_id, Food_id, Food_qty, Total_price) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    handle_database_operation(query, tuple(values))


def view_records():
    """Displays records from the database"""
    print("\n--- View Records ---")
    options = {
        1: ("Employee", "Employee", "Emp_id"),
        2: ("Customer", "Customer", "c_id"),
        3: ("Food Items", "Food", None),
        4: ("Orders", "OrderFood", "OrderF_id")
    }

    for key, value in options.items():
        print(f"{key}. View {value[0]}")

    choice = get_valid_input("Enter your choice (1-4): ", int)

    if choice not in options:
        print("Invalid choice")
        return

    table, column = options[choice][1], options[choice][2]
    if column:
        search_value = get_valid_input(f"Enter {column} to search: ", int)
        query = f"SELECT * FROM {table} WHERE {column} = %s"
        results = handle_database_operation(query, (search_value,), fetch=True)
    else:
        query = f"SELECT * FROM {table}"
        results = handle_database_operation(query, fetch=True)

    if results:
        print(f"\n{table} Records:")
        for row in results:
            print(row)
    else:
        print("No records found.")


def update_payment_status():
    """Updates customer payment status"""
    print("\n--- Update Payment Status ---")
    c_id = get_valid_input("Enter Customer ID: ", int)
    new_status = get_valid_input("Enter new payment status (Paid/Unpaid): ", str)

    query = "UPDATE Customer SET pstatus = %s WHERE c_id = %s"
    handle_database_operation(query, (new_status, c_id))


def clear_screen():
    """Clears the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def main_menu():
    """Displays the main menu and handles user input"""
    menu_options = {
        1: ("Add Employee", add_employee),
        2: ("Add Customer", add_customer),
        3: ("Add Food Item", add_food_item),
        4: ("Add Order", add_order),
        5: ("Update Payment Status", update_payment_status),
        6: ("View Records", view_records),
        7: ("Exit", exit)
    }

    while True:
        clear_screen()
        print("\n=== Food Ordering System ===")
        for key, value in menu_options.items():
            print(f"{key}. {value[0]}")

        try:
            choice = int(input("\nEnter your choice (1-7): "))
            if choice == 7:
                print("Exiting program...")
                break

            if choice in menu_options:
                menu_options[choice][1]()
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")

        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
