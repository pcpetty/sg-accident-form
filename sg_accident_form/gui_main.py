import tkinter as tk
from tkinter import messagebox, font, filedialog
import threading
from sg_accident_form.db_operations import insert_into_postgresql, connect_postgresql
import sg_accident_form.utils as utils
import os
from fpdf import FPDF
import re

# Validation Functions
def validate_text_input(value):
    """Validates text input to ensure it is not empty."""
    if value.strip():
        return True
    else:
        messagebox.showwarning("Invalid Input", "This field cannot be empty.")
        return False

def validate_date_input(value):
    """Validates date input in MM/DD/YYYY format."""
    date_pattern = r"^(0[1-9]|1[0-2])/([0-2][0-9]|3[01])/\d{4}$"
    if re.match(date_pattern, value):
        return True
    else:
        messagebox.showwarning("Invalid Date", "Enter date in MM/DD/YYYY format.")
        return False

def validate_time_input(value):
    """Validates time input in HH:MM 24-hour format."""
    time_pattern = r"^([01][0-9]|2[0-3]):[0-5][0-9]$"
    if re.match(time_pattern, value):
        return True
    else:
        messagebox.showwarning("Invalid Time", "Enter time in HH:MM format.")
        return False

def clear_fields(entries, dropdown=None):
    """Clears all input fields and resets dropdown."""
    for entry in entries:
        entry.delete(0, tk.END)
    if dropdown:
        dropdown.set("SAF")

# FLT Number Functions
def get_next_flt_number(connection):
    """Fetches the next FLT number from the database."""
    query = "SELECT nextval('flt_sequence') AS next_flt;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        return result["next_flt"] if result else None

def fetch_flt_number():
    """Fetches the next FLT number."""
    connection = connect_postgresql()
    if connection:
        flt_number = get_next_flt_number(connection)
        connection.close()
        return flt_number
    else:
        messagebox.showerror("Error", "Database connection failed.")
        return None

# Generate PDF
def generate_pdf(data):
    """Generates a PDF from the accident report data."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Accident Report", ln=True, align="C")
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_path:
        pdf.output(output_path)
        return output_path
    else:
        return None

# Submit Form
def submit_form():
    """Handles form submission."""
    data = {
        "Driver Name": driver_name_entry.get(),
        "Driver ID": driver_id_entry.get(),
        "Accident Location": accident_location_entry.get(),
        "Accident Date": accident_date_entry.get(),
        "Accident Time": accident_time_entry.get(),
        "Division": selected_division.get()
    }

    # Validate inputs
    if not all([
        validate_text_input(data["Driver Name"]),
        validate_text_input(data["Driver ID"]),
        validate_text_input(data["Accident Location"]),
        validate_date_input(data["Accident Date"]),
        validate_time_input(data["Accident Time"])
    ]):
        return

    # Fetch FLT number
    flt_number = fetch_flt_number()
    if not flt_number:
        return

    data["FLT Number"] = flt_number

    # Generate PDF
    pdf_path = generate_pdf(data)
    if not pdf_path:
        return

    # Submit to database
    def task():
        try:
            insert_into_postgresql(data)
            messagebox.showinfo("Success", "Report submitted successfully!")
            clear_fields([driver_name_entry, driver_id_entry, accident_location_entry, accident_date_entry, accident_time_entry], selected_division)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit report: {e}")

    threading.Thread(target=task).start()

# GUI Initialization
root = tk.Tk()
root.title("Safety Generalist Accident Report Form")
root.geometry("600x700")
root.configure(bg="#f0f0f0")

custom_font = font.Font(family="Arial", size=12)
root.option_add("*Font", custom_font)

# Logo
tk.Label(root, text="RISK RANGER", font=("Courier", 24, "bold"), fg="blue", bg="#f0f0f0").pack(pady=10)

# Form Fields
driver_name_entry = tk.Entry(root)
tk.Label(root, text="Driver Name:").pack(pady=5)
driver_name_entry.pack(pady=5)

driver_id_entry = tk.Entry(root)
tk.Label(root, text="Driver ID:").pack(pady=5)
driver_id_entry.pack(pady=5)

accident_location_entry = tk.Entry(root)
tk.Label(root, text="Accident Location:").pack(pady=5)
accident_location_entry.pack(pady=5)

accident_date_entry = tk.Entry(root)
tk.Label(root, text="Accident Date (MM/DD/YYYY):").pack(pady=5)
accident_date_entry.pack(pady=5)

accident_time_entry = tk.Entry(root)
tk.Label(root, text="Accident Time (HH:MM):").pack(pady=5)
accident_time_entry.pack(pady=5)

selected_division = tk.StringVar(value="SAF")
tk.Label(root, text="Division:").pack(pady=5)
division_dropdown = tk.OptionMenu(root, selected_division, "SAF", "INMO", "CLP")
division_dropdown.pack(pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", bg="green", fg="white", font=("Helvetica", 12, "bold"), command=submit_form)
submit_button.pack(pady=20)

# Run Application
if __name__ == "__main__":
    root.mainloop()
