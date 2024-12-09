# import tkinter as tk
# from tkinter import messagebox
# from sg_accident_form.db_operations import insert_into_postgresql
# from sg_accident_form.utils import get_date

# def submit_form():
#     driver_name = driver_name_entry.get()
#     accident_location = accident_location_entry.get()
#     accident_date = get_date("Enter accident date (MM/DD/YYYY): ")

#     if driver_name and accident_location and accident_date:
#         accident_data = {
#             "driver_name": driver_name,
#             "accident_location": accident_location,
#             "accident_date": accident_date
#         }
#         insert_into_postgresql(accident_data)
#         messagebox.showinfo("Submission Successful", f"Report for {driver_name} submitted!")
#     else:
#         messagebox.showwarning("Incomplete Data", "Please fill in all fields.")

# # Initialize main window
# root = tk.Tk()
# root.title("Safety Generalist Accident Report Form")
# root.geometry("400x300")

# # Driver Name Field
# tk.Label(root, text="Driver Name:").pack(pady=5)
# driver_name_entry = tk.Entry(root)
# driver_name_entry.pack(pady=5)

# # Accident Location Field
# tk.Label(root, text="Accident Location:").pack(pady=5)
# accident_location_entry = tk.Entry(root)
# accident_location_entry.pack(pady=5)

# # Submit Button
# submit_button = tk.Button(root, text="Submit", command=submit_form)
# submit_button.pack(pady=20)

# # Run the application
# root.mainloop()

# # SETUP>PY INTEGRATION FOR ENTRY POINT
# from setuptools import setup, find_packages

# setup(
#     name="sg_accident_form",
#     version="1.1.2",
#     description="Safety Generalist Accident Reporting System",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     author="Cole Petty",
#     author_email="colepetty57@gmail.com",
#     url="https://github.com/pcpetty/sg_accident_form",
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         "fpdf2>=2.7.0",
#         "psycopg2>=2.9.0",
#         "questionary>=1.10.0",
#         "openpyxl>=3.1.0",
#     ],
#     python_requires=">=3.8",
#     entry_points={
#         "console_scripts": [
#             "sg-accident-form=sg_accident_form.main:main",   # CLI entry point
#             "sg-accident-form-gui=gui_main:submit_form",     # GUI entry point
#         ],
#     },
#     classifiers=[
#         "Programming Language :: Python :: 3.8",
#         "License :: Other/Proprietary License",
#         "Operating System :: OS Independent",
#     ],
# )


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
