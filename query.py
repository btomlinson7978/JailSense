import sqlite3
from prettytable import PrettyTable

def showTables():
    # Query to fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Fetch and print all table names
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])

# Function to describe any table
def describe_table(table_name):
    # Connect to the database
    connection = sqlite3.connect("JIMS.db")
    cursor = connection.cursor()

    # Query to get the table schema (column names and types)
    cursor.execute(f"PRAGMA table_info({table_name});")

    # Fetch the column information
    columns = cursor.fetchall()

    # Create a PrettyTable object to format the output
    table = PrettyTable()

    # Define the column names for the grid
    table.field_names = ["Column ID", "Column Name", "Data Type", "Not Null", "Default Value", "Primary Key"]

    # Add each column's details to the table
    for column in columns:
        table.add_row(column)

    # Print the table description
    print(f"Description of the '{table_name}' table:")
    print(table)

    # Close the connection
    connection.close()


# Method to add a new admin user
def add_admin(name, dob, clearance, username, password):
    # Connect to the database
    connection = sqlite3.connect("JIMS.db")
    cursor = connection.cursor()
    # Insert the new admin into the 'admins' table
    cursor.execute("""
    INSERT INTO admins (Name, DateOfBirth, AdminClearance, Username, Password)
    VALUES (?, ?, ?, ?, ?);
    """, (name, dob, clearance, username, password))
    # Commit the transaction
    connection.commit()
    # Close the connection
    connection.close()
    print(f"New admin '{name}' added successfully.")

def show_table_contents(table_name):
    # Connect to the database
    connection = sqlite3.connect("JIMS.db")
    cursor = connection.cursor()
    try:
        # Query to select all rows from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        # Fetch all rows
        rows = cursor.fetchall()
        # Create a PrettyTable to display the data
        if rows:
            # Get column names (add 'ROWID' as the first column)
            column_names = ["ID"] + [description[0] for description in cursor.description][1:]
            table = PrettyTable(column_names)
            
            # Add rows to the table
            for row in rows:
                table.add_row(row)

            # Print the table to the console
            print(table)
        else:
            print(f"No data found in {table_name}.")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the connection
        connection.close()

connection = sqlite3.connect("JIMS.db")
cursor = connection.cursor()

######################################
######################################

connection.commit()
connection.close()