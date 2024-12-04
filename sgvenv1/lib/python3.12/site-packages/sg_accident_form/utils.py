# SG Accident Report Utilities 

# Import Libraries and Modules
import datetime
import questionary
import json
import PyQt6
import re
import json

# Date input function with default pass
def get_date(prompt):
    while True:
        date_str = input(f"{prompt} (Press Enter to skip): ").strip()
        if not date_str:  # Allow skipping
            return None
        try:
            return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY or press Enter to skip.")

# Time input function with default pass
def get_time():
    while True:
        time_str = input("Enter time (HH:MM) or press Enter to skip: ").strip()
        if not time_str:  # Allow skipping
            return None
        try:
            return datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please use HH:MM or press Enter to skip.")

# Input with Default
def input_with_default(prompt, default):
    response = input(f"{prompt} (Press Enter to default to '{default}'): ").strip()
    return response if response else default

# Yes/No Input with Default
def get_yes_no(prompt, default="no"):
    while True:
        response = input_with_default(prompt, default).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n', or press Enter to skip.")

# Reusable function for selecting conditions
def get_condition(condition_type, choices):
    """
    Provides a selection prompt for specific conditions.
    """
    try:
        choice = questionary.select(
            f"Choose {condition_type.replace('_', ' ')}:",
            choices=choices + ['Custom']
        ).ask()
        if choice == "Custom":
            return input(f"Enter custom {condition_type.replace('_', ' ')}: ").strip()
        return choice
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Regex validation for phone numbers
def validate_phone(prompt):
    while True:
        phone = input(prompt).strip()
        if re.match(r'^\+?1?\d{10,15}$', phone):  # Allows international format or 10-15 digits
            return phone
        print("Invalid phone number. Please enter a valid phone number (e.g., 1234567890 or +11234567890).")

# Regex validation for license plate
def validate_license_plate(prompt):
    while True:
        plate = input(prompt).strip()
        if not plate:
            return None
        if re.match(r'^[A-Z0-9]{1,8}$', plate):  # Allows up to 8 alphanumeric characters
            try:
                return plate
            except ValueError:
                pass
        print("Invalid license plate. Please enter a valid license plate (e.g., ABC1234).")

# Regex validation for date (MM/DD/YYYY)
def validate_date(prompt):
    while True:
        date_str = input(f"{prompt} (Press Enter to skip): ").strip()
        if not date_str:  # Allow skipping
            return None
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            try:
                return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                pass
        print("Invalid date format. Please use MM/DD/YYYY.")

# Regex validation for email
def validate_email(prompt):
    while True:
        email = input(prompt).strip()
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  # Basic email validation
            return email
        print("Invalid email address. Please enter a valid email address.")

# Clean up report for sql storage        
def clean_field(field):
    return field.strip() if field else None

