import tkinter as tk
from tkinter import messagebox
import threading
from sg_accident_form.db_operations import insert_into_postgresql
from sg_accident_form.data_collection import collect_accident_data
import sg_accident_form.utils as utils

# Initialize main window
root = tk.Tk()
root.title("Safety Generalist Accident Report Form")
root.geometry("600x700")
root.configure(bg="#f0f0f0")

# Display the RiskRanger logo
def display_logo():
    logo_text = "RISK RANGER"
    logo_label = tk.Label(root, text=logo_text, font=("Courier", 24, "bold"), fg="blue", bg="#f0f0f0")
    logo_label.pack(pady=10)

display_logo()

# Fields for the form
tk.Label(root, text="Driver Name:", bg="#f0f0f0").pack(pady=5)
driver_name_entry = tk.Entry(root)
driver_name_entry.pack(pady=5)

tk.Label(root, text="Accident Location:", bg="#f0f0f0").pack(pady=5)
accident_location_entry = tk.Entry(root)
accident_location_entry.pack(pady=5)

tk.Label(root, text="Accident Date (MM/DD/YYYY):", bg="#f0f0f0").pack(pady=5)
accident_date_entry = tk.Entry(root)
accident_date_entry.pack(pady=5)

# Submit Button with threading
def submit_form():
    driver_name = driver_name_entry.get()
    accident_location = accident_location_entry.get()
    accident_date = accident_date_entry.get()

    if utils.validate_input(driver_name, "Driver Name") and utils.validate_input(accident_location, "Accident Location") and utils.validate_date(accident_date):
        accident_data = {
            "driver_name": driver_name,
            "accident_location": accident_location,
            "accident_date": accident_date
        }

        def task():
            try:
                insert_into_postgresql(accident_data)
                messagebox.showinfo("Success", "Report submitted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Submission failed: {e}")

        threading.Thread(target=task).start()
    else:
        messagebox.showwarning("Incomplete Data", "Please fill in all fields.")

submit_button = tk.Button(root, text="Submit", bg="green", fg="white", font=("Helvetica", 12, "bold"), command=submit_form)
submit_button.pack(pady=20)

# Run the application
if __name__ == "__main__":
    root.mainloop()

# #"""
# sg-accident-form/
# │
# ├── sg_accident_form/
# │   ├── __init__.py
# │   ├── main.py                 # CLI entry point
# │   ├── db_operations.py
# │   ├── data_collection.py
# │   ├── report_generation.py
# │   └── utils.py
# │
# ├── gui_main.py                 # GUI entry point (placed in the main folder)
# │
# ├── setup.py                    # Packaging configuration
# ├── README.md                   # Project documentation
# └── requirements.txt            # Dependencies
# REINSTALL PACKAGE
# RUN
# sg-accident-form-gui

# Packaging the GUI as an Executable

# To create a Windows executable (.exe) for the GUI using PyInstaller:

# Install PyInstaller (if not already installed):
# pip install pyinstaller
# pyinstaller --onefile --windowed sg_accident_form/gui_main.py
# --onefile: Package everything into a single .exe file.
# --windowed: Prevent a console window from appearing (for GUI applications).
# dist/gui_main.exe

## CONNECT TO PSQL
# from db_operations import connect_postgresql, insert_into_postgresql

# def submit_form():
#     driver_name = driver_name_entry.get()
#     accident_location = accident_location_entry.get()

#     if driver_name and accident_location:
#         accident_data = {
#             "driver_name": driver_name,
#             "accident_location": accident_location
#         }
#         insert_into_postgresql(accident_data)
#         messagebox.showinfo("Submission Successful", f"Report for {driver_name} submitted!")
#     else:
#         messagebox.showwarning("Incomplete Data", "Please fill in all fields.")


# ICONS AND BRANDING 5. Optional Enhancements

# Add Icons and Branding:

# Use the --icon flag with PyInstaller to include a custom icon:

# pyinstaller --onefile --windowed --icon=app_icon.ico your_script.py
