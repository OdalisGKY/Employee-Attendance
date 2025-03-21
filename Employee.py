import matplotlib.pyplot as plt
from prettytable import PrettyTable
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# File to store employee data
DATA_FILE = 'employee_data.json'

# Load employee data from a JSON file
def load_employee_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {
        "Tim": ["2025-03-01", "2025-03-05"],
        "Tom": ["2025-03-02", "2025-03-03", "2025-03-04", "2025-03-10"],
        "John": ["2025-03-15"],
        "Jedi": ["2025-03-01", "2025-03-02", "2025-03-05", "2025-03-10", "2025-03-20"],
        "Kat": [],
        "Jim": ["2025-03-12"],
        "Sharon": ["2025-03-14", "2025-03-15", "2025-03-16"],
        "Wayne": ["2025-03-01", "2025-03-02", "2025-03-03", "2025-03-04", "2025-03-05", "2025-03-06"],
        "Brian": ["2025-03-07"],
        "Pam": [],
        "Quaita": ["2025-03-08", "2025-03-09"],
        "Brandy": ["2025-03-11", "2025-03-12", "2025-03-13"],
        "Greg": ["2025-03-14", "2025-03-15", "2025-03-16", "2025-03-17", "2025-03-18", "2025-03-19", "2025-03-20"]
    }

# Save employee data to a JSON file
def save_employee_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Display attendance in a table
def display_attendance(data):
    table = PrettyTable()
    table.field_names = ["Employee", "Missed Days", "Dates Missed"]

    for employee, missed_dates in data.items():
        missed_days_count = len(missed_dates)
        missed_dates_str = ", ".join(missed_dates)

        # Highlight employees with more than 3 missed days
        if missed_days_count > 3:
            table.add_row([f"\033[91m{employee}\033[0m", missed_days_count, missed_dates_str])  # Red text for high absences
        else:
            table.add_row([employee, missed_days_count, missed_dates_str])

    print(table)

# Create a bar chart
def plot_attendance(data, month):
    names = list(data.keys())
    missed_days = [len(dates) for dates in data.values()]

    plt.bar(names, missed_days, color=['red' if days > 3 else 'blue' for days in missed_days])
    plt.xlabel('Employees')
    plt.ylabel('Missed Days')
    plt.title(f'Employee Attendance for {month}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to update missed days
def update_missed_days(employee_name, days_missed):
    if days_missed == 0:
        employees[employee_name] = []  # Clear missed days if 0 is entered
    else:
        # Add dummy dates for missed days
        for _ in range(days_missed):
            employees[employee_name].append("2025-03-20")  # Use a placeholder date

# GUI for input
def gui_input():
    while True:
        response = simpledialog.askstring("Input", "Do you want to input data? (Yes/No)")
        if response and response.lower() == 'yes':
            employee_name = simpledialog.askstring("Input", "Enter the employee's name:").strip()
            # Check for case-insensitive matching
            matched_employee = next((name for name in employees.keys() if name.lower() == employee_name.lower()), None)
            if matched_employee:
                days_missed = simpledialog.askinteger("Input", "Enter number of missed days:")
                if days_missed is not None:  # Allow '0' for no missed days
                    update_missed_days(matched_employee, days_missed)
                    messagebox.showinfo("Success", f"Updated {matched_employee}'s missed days.")
                else:
                    messagebox.showwarning("Input Error", "Please enter a valid number of missed days.")
            else:
                messagebox.showwarning("Input Error", "Employee not found.")
        elif response and response.lower() == 'no':
            add_employee_response = simpledialog.askstring("Input", "Do you want to add another employee? (Yes/No)")
            if add_employee_response and add_employee_response.lower() == 'yes':
                new_employee_name = simpledialog.askstring("Input", "Enter the new employee's name:").strip()
                if new_employee_name and new_employee_name not in employees:
                    employees[new_employee_name] = []  # Add new employee with no missed days
                    messagebox.showinfo("Success", f"Added new employee: {new_employee_name}.")
                else:
                    messagebox.showwarning("Input Error", "Invalid employee name or employee already exists.")
            else:
                break

#  Main function
def main():
    global employees
    employees = load_employee_data()  # Load employee data
    current_month = datetime.now().strftime("%B %Y")  # Get current month and year
    display_attendance(employees)  # Display attendance first
    gui_input()  # Start GUI input
    save_employee_data(employees)  # Save employee data before exiting
    plot_attendance(employees, current_month)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    main()