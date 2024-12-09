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
    """
    Prompt the user for a date input in MM/DD/YYYY format with the option to skip.
    Validates the format using regex before parsing.
    """
    while True:
        date_str = input(f"{prompt} (Press Enter to skip): ").strip()
        if not date_str:
            return None
        if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            try:
                return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                print("Invalid date. Please ensure the date is valid (e.g., 02/30/2024 is not valid).")
        else:
            print("Invalid format. Please use MM/DD/YYYY.")

# Time input function with default pass
def get_time(prompt="Enter time (HH:MM) or press Enter to skip: "):
    """
    Prompt the user for a time input in HH:MM format with the option to skip.
    Validates the format using regex before parsing.
    """
    while True:
        time_str = input(prompt).strip()
        if not time_str:
            return None
        if re.match(r'^\d{2}:\d{2}$', time_str):
            try:
                return datetime.datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                print("Invalid time. Please ensure the time is valid (e.g., 25:61 is not valid).")
        else:
            print("Invalid format. Please use HH:MM.")

# Input with Default
def input_with_default(prompt, default):
    """
    Prompt the user for input with the option to default if input is empty.
    Handles interruptions gracefully.
    """
    try:
        response = input(f"{prompt} (Press Enter to default to '{default}'): ").strip()
        return response if response else default
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Defaulting to provided value.")
        return default

def get_yes_no(prompt, default="no"):
    """
    Prompt the user for a yes/no response with the option to default.
    Handles invalid inputs and interruptions gracefully.
    """
    valid_yes = ['y', 'yes']
    valid_no = ['n', 'no']
    
    while True:
        try:
            response = input_with_default(prompt, default).lower()
            if response in valid_yes:
                return True
            elif response in valid_no:
                return False
            else:
                print(f"Invalid input. Please enter 'y' for yes or 'n' for no, or press Enter to default to '{default}'.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Defaulting to 'no'.")
            return False

# Reusable function for selecting conditions

def get_condition(condition_type, choices):
    """
    Prompt the user to select a condition from a list or enter a custom value.
    Handles interruptions and ensures input is sanitized.
    """
    try:
        choice = questionary.select(
            f"Choose {condition_type.replace('_', ' ')}:",
            choices=choices + ['Custom', 'Skip']
        ).ask()

        if choice == "Custom":
            custom_input = input(f"Enter custom {condition_type.replace('_', ' ')}: ").strip()
            # Sanitize input for PostgreSQL (basic sanitization)
            sanitized_input = re.sub(r'[^\w\s\-]', '', custom_input)
            return sanitized_input

        if choice == "Skip":
            print(f"{condition_type.replace('_', ' ')} skipped.")
            return None

        return choice
    except (EOFError, KeyboardInterrupt):
        print(f"\nInput interrupted. Skipping {condition_type.replace('_', ' ')}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
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
# def validate_date(prompt):
#     while True:
#         date_str = input(f"{prompt} (Press Enter to skip): ").strip()
#         if not date_str:  # Allow skipping
#             return None
#         if re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
#             try:
#                 return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
#             except ValueError:
#                 pass
#         print("Invalid date format. Please use MM/DD/YYYY.")

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

