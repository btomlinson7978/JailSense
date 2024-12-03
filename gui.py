import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Function to check login credentials
def check_login(username, password):
    connection = sqlite3.connect("JIMS.db") # connect to the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admins WHERE Username = ? AND Password = ?", (username, password)) # query execution for username and password
    user = cursor.fetchone()
    connection.close()

    if user: # if admin is in database, proceed
        return True
    else:
        return False

# Create a new window for the Inmate Registry
def open_inmate_registry():
    registry_window = tk.Tk()
    registry_window.title("Inmate Registry")
    window_width = 800
    window_height = 600
    center_window(registry_window, window_width, window_height)

    # Add buttons for the registry actions
    add_inmate_button = tk.Button(registry_window, text="Add Inmate", command=lambda: add_inmate(registry_window))
    add_inmate_button.pack(pady=20)
    search_inmate_button = tk.Button(registry_window, text="Search Inmate", command=lambda: search_inmate(registry_window))
    search_inmate_button.pack(pady=20)
    remove_inmate_button = tk.Button(registry_window, text="Remove Inmate", command=lambda: remove_inmate(registry_window))
    remove_inmate_button.pack(pady=20)
    display_all_inmates_button = tk.Button(registry_window, text="Display All Inmates", command=lambda: display_all_inmates())
    display_all_inmates_button.pack(pady=20)

    registry_window.mainloop() # open the registry window

# Button to display all inmates
def display_all_inmates():
    all_inmates_window = tk.Toplevel()
    all_inmates_window.title("All Inmates")
    center_window(all_inmates_window, 400, 400)

    # Connect to the database
    connection = sqlite3.connect("JIMS.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM inmates") # Query to get all inmate names
    inmates = cursor.fetchall()

    # Display the inmate names in a list
    if inmates:
        for index, inmate in enumerate(inmates):
            tk.Label(all_inmates_window, text=f"{index + 1}. {inmate[0]}").pack(pady=5)
    else:
        tk.Label(all_inmates_window, text="No inmates found.").pack(pady=20)

    connection.close() # Close the connection
    back_button = tk.Button(all_inmates_window, text="Back", command=all_inmates_window.destroy) # Add the "Back" button
    back_button.pack(pady=20)

    all_inmates_window.mainloop() # open the display all inmates window

# Button to add one new inmate
def add_inmate(parent_window):
    add_inmate_window = tk.Toplevel(parent_window)
    add_inmate_window.title("Add Inmate")
    center_window(add_inmate_window, 400, 700)

    # Define field names and create labels and text boxes for each field
    fields = [
        ("Name", ""),
        ("AKAs", ""),
        ("DateofBirth", ""),
        ("Residence", ""),
        ("Employment", ""),
        ("PhysicalDescription", ""),
        ("ApparentHealth", ""),
        ("ArrestingOfficer", ""),
        ("ArrestingAgency", ""),
        ("LocationOfArrest", ""),
        ("DetentionFacility", ""),
        ("FacilityTransfers", ""),
        ("ScheduledCourtAppearances", ""),
        ("ScheduledClinicVisits", ""),
        ("PersonalProperty", ""),
        ("InmateBail", "")
    ]
    entries = {}
    
    # Create the labels and text boxes in a grid
    for idx, (field, default) in enumerate(fields):
        label = tk.Label(add_inmate_window, text=field)
        label.grid(row=idx, column=0, sticky="e", padx=10, pady=5)
        entry = tk.Entry(add_inmate_window)
        entry.insert(0, default)
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
        entries[field] = entry
    
    # submit button 
    def submit_inmate():
        values = [entry.get() for entry in entries.values()] # Collect values from entries
        print("Form data:", values) # Print values to check if the form data is being collected correctly

        # Check if all fields are filled
        if any(value == "" for value in values):
            tk.messagebox.showerror("Error", "All fields must be filled!")
            return

        # Connect to the database and insert the new inmate data
        try:
            connection = sqlite3.connect("JIMS.db")
            cursor = connection.cursor()

            # text query to add inmate information from user into the database inmate table 
            cursor.execute("""
                INSERT INTO inmates (Name, AKAs, DateOfBirth, Residence, Employment, PhysicalDescription, 
                                    ApparentHealth, ArrestingOfficer, ArrestingAgency, LocationOfArrest, DetentionFacility, 
                                    FacilityTransfers, ScheduledCourtAppearances, ScheduledClinicVisits, PersonalProperty, InmateBail)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(values))
            
            # commit, close, display successful addition of info
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("Success", "Inmate added successfully.")
            print("Inmate added to database.")
        
            add_inmate_window.destroy() # Close the Add Inmate window
        
        except Exception as e:
            # Handle errors and show an error message
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print("Error:", e)

    # submit button 
    submit_button = tk.Button(add_inmate_window, text="Submit", command=submit_inmate)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # back button
    back_button = tk.Button(add_inmate_window, text="Back", command=add_inmate_window.destroy)
    back_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

    add_inmate_window.mainloop() # open the Add Inmate window

# Button for inmate search
def search_inmate(parent_window):
    # Create a new window for searching an inmate
    search_inmate_window = tk.Toplevel(parent_window)
    search_inmate_window.title("Search Inmate")
    center_window(search_inmate_window, 400, 300)
    name_label = tk.Label(search_inmate_window, text="Inmate Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(search_inmate_window)
    name_entry.pack(pady=5)

    # Function to search for the inmate
    def search_inmate():
        name = name_entry.get()
        if not name:
            tk.messagebox.showerror("Error", "Please enter an inmate name")
            return

        connection = sqlite3.connect("JIMS.db") 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM inmates WHERE Name=?", (name,)) # Query to search for the inmate
        inmate = cursor.fetchone() # inmate obtained from cursor query 

        if inmate:
            # Display inmate details
            info_window = tk.Toplevel(search_inmate_window)
            info_window.title("Inmate Information")

            details = [
                f"Name: {inmate[1]}",
                f"AKAs: {inmate[2]}",
                f"Date Of Birth: {inmate[3]}",
                f"Residence: {inmate[4]}",
                f"Employment: {inmate[5]}",
                f"Physical Description: {inmate[6]}",
                f"Apparent Health: {inmate[7]}",
                f"Arresting Officer: {inmate[8]}",
                f"Arresting Agency: {inmate[9]}",
                f"Location of Arrest: {inmate[10]}",
                f"Detention Facility: {inmate[11]}",
                f"Facility Transfers: {inmate[12]}",
                f"Court Appearances: {inmate[13]}",
                f"Clinic Visits: {inmate[14]}",
                f"Personal Property: {inmate[15]}",
                f"Bail: {inmate[16]}"
            ]

            for detail in details:
                tk.Label(info_window, text=detail).pack(pady=5)

        else:
            tk.messagebox.showerror("Not Found", "Inmate not found")

        connection.close()

    
    search_button = tk.Button(search_inmate_window, text="Search", command=search_inmate) # Search button   
    search_button.pack(pady=10)
    back_button = tk.Button(search_inmate_window, text="Back", command=search_inmate_window.destroy) # Back button 
    back_button.pack(pady=10)

    search_inmate_window.mainloop() # Start the search inmate window

# Button to remove inmate upon search
def remove_inmate(parent_window):
    remove_inmate_window = tk.Toplevel(parent_window) # create window
    remove_inmate_window.title("Remove Inmate")
    center_window(remove_inmate_window, 400, 200)

    # label and text box to enter the name of the inmate to remove
    name_label = tk.Label(remove_inmate_window, text="Inmate Name to Remove:")
    name_label.pack(pady=10)
    name_entry = tk.Entry(remove_inmate_window)
    name_entry.pack(pady=10)

    # Function to remove the inmate from the database
    def remove_inmate():
        name = name_entry.get()
        if not name:
            tk.messagebox.showerror("Error", "Please enter an inmate name")
            return

        # Connect to the database and delete the inmate
        connection = sqlite3.connect("JIMS.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inmates WHERE Name=?", (name,))
        connection.commit()

        # Show confirmation or error
        if cursor.rowcount > 0:
            tk.messagebox.showinfo("Success", f"Inmate {name} has been removed.")
        else:
            tk.messagebox.showerror("Not Found", "Inmate not found")

        # Close the connection
        connection.close()

    remove_button = tk.Button(remove_inmate_window, text="Remove", command=remove_inmate) # Remove button
    remove_button.pack(pady=10)
    back_button = tk.Button(remove_inmate_window, text="Back", command=remove_inmate_window.destroy) # Back button
    back_button.pack(pady=10)

    remove_inmate_window.mainloop() # Start the remove inmate window


global login_window
login_window = tk.Tk()
login_window.title("Admin Login")
center_window(login_window, 400, 400)

# username and password fields
username_label = tk.Label(login_window, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=10)
password_label = tk.Label(login_window, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=10)

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check login credentials
    if check_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome!")
        login_window.destroy() #close login after user logs in
        open_inmate_registry()
    else:
        messagebox.showerror("Error", "Invalid login credentials!")

# Add login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack(pady=20)

# Start the login window
login_window.mainloop()
