from .db_operations import connect_postgresql, insert_into_postgresql, get_next_flt_number, load_report, edit_report_field
from .report_generation import export_to_excel, export_to_pdf, save_to_json
from .utils import get_yes_no, input_with_default
from .data_collection import collect_accident_data, dot_recordable, post_accident_testing, post_accident_testing_timeline, followup_needed, citation_info
import pyfiglet
from datetime import datetime
import shutil
import os
from pathlib import Path
from fpdf import FPDF
from colorama import init, Fore, Style


# Initialize colorama for Windows compatibility (optional on Unix systems)
init(autoreset=True)

def tutorial():
    """
    Provides a step-by-step tutorial on accident reporting.
    """
    print("\nAccident Reporting SOP Tutorial:")
    steps = [
        "First determine if anyone is injured.",
        "Ask for the basic vehicle information before taking a statement from the driver.",
        "Once a statement is obtained, determine if this is an accident or an incident.",
        "Ask for pictures of all vehicles involved from all four sides from a wide angle.",
        "Obtain other motorists' contact and insurance information.",
        "If police are involved, determine if a citation has been issued.",
        "If a citation has been issued, proceed with the post-accident testing SOP.",
        "If any injuries are sustained, determine if EMS will transport anyone from the scene. If so, where are they being transported?",
        "If a tow is required, determine if the vehicle is disabled. If it is being towed, obtain the tow company information.",
    ]
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step}")
        if not get_yes_no("Do you want to continue the tutorial? (y/n)", "yes"):
            print("\nTutorial skipped. Proceeding to the form...")
            break
    else:
        print("\nTutorial Complete. Proceeding to the form...")

def display_logo(context="startup", reference_id=None):
    """
    Displays the RiskRanger logo with different messages based on context.

    Args:
        context (str): Determines the message displayed. Options: 'startup', 'submission'.
        reference_id (str): The reference ID for submission confirmation (optional).
    """
    # Generate the ASCII logo
    logo = pyfiglet.figlet_format("RiskRanger")

    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Center the logo horizontally
    centered_logo = "\n".join(
        line.center(terminal_width) for line in logo.split("\n")
    )

    # Define the content based on context
    if context == "startup":
        lines = [
            "A SAFETY & RISK MANAGEMENT SOLUTION",
            "Welcome to the Safety Generalist Accident Report Form!",
        ]
    elif context == "submission" and reference_id:
        lines = [
            "A SAFETY & RISK MANAGEMENT SOLUTION",
            "Your report has been submitted successfully to RiskRanger!",
            f"Reference ID: {reference_id}",
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Thank you for choosing RiskRanger for safety and risk reporting.",
        ]
    else:
        lines = ["A SAFETY & RISK MANAGEMENT SOLUTION"]

    # Define the width of the box
    box_width = 80  # Fixed width for the box

    # Generate the border box
    border_top_bottom = "█" + " " * (box_width - 2) + "█"
    content_lines = [
        "█" + line.center(box_width - 2) + "█" for line in lines
    ]

    # Legal notice
    legal_notice = "© 2024 RiskRanger. All Rights Reserved. Unauthorized use prohibited."
    legal_line = "█" + legal_notice.center(box_width - 2) + "█"

    # Center the entire box
    padding = (terminal_width - box_width) // 2
    padded_border = " " * padding + border_top_bottom
    padded_content = "\n".join(" " * padding + line for line in content_lines)
    padded_legal_line = " " * padding + legal_line

    # Display everything
    print(centered_logo)
    print(padded_border)
    print(padded_content)
    print(padded_legal_line)
    print(padded_border)
    print("\n")

from sg_accident_form.gui_main import root
from sg_accident_form.data_collection import collect_accident_data

def main():
    print("Choose an option:")
    print("1. Run CLI")
    print("2. Run GUI")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        accident_data = collect_accident_data()
        print("Collected Data:", accident_data)
    elif choice == "2":
        root.mainloop()
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()

def main():
    try:
        display_logo(context="startup")
        print(Fore.CYAN + "Safety Generalist Accident Report Form")

        while True:  # Main menu loop
            print("\n" + Fore.GREEN + "Options:")
            print(Fore.YELLOW + "1. Create a new report")
            print(Fore.YELLOW + "2. Edit an existing report")
            print(Fore.YELLOW + "3. Exit")

            choice = input_with_default(Fore.MAGENTA + "Choose an option (1/2/3): ", "3")

            if choice == "1":
                # Optional SOP Tutorial
                if get_yes_no(Fore.CYAN + "Would you like an accident reporting SOP tutorial? (y/n): ", "no"):
                    tutorial()

                # Collect new accident data
                accident_data = collect_accident_data()

                while True:  # Retry mechanism for FLT number generation and submission
                    reference_key = get_next_flt_number()
                    print(f"Generated reference key: {reference_key}")
                    if reference_key:
                        accident_data["reference_key"] = reference_key

                        # Save data
                        save_to_json(accident_data)
                        insert_into_postgresql(accident_data)
                        try:
                            export_to_excel(accident_data, filename=f"{reference_key}.xlsx")
                        except Exception as e:
                            print(f"Error exporting to Excel: {e}")
                        try:
                            export_to_pdf(accident_data, filename=f"{reference_key}.pdf")
                        except Exception as e:
                            print(f"Error while generating PDF: {e}")
                        
                        # Ensure the output directory exists
                        output_dir = Path.home() / "accident_reports"
                        output_dir.mkdir(exist_ok=True)

                        # Update file paths for export
                        excel_filename = output_dir / f"{reference_key}.xlsx"
                        pdf_filename = output_dir / f"{reference_key}.pdf"
                        export_to_excel(accident_data, filename=excel_filename)
                        export_to_pdf(accident_data, filename=pdf_filename)

                        # Display the submission confirmation
                        display_logo(context="submission", reference_id=reference_key)

                        # Exit the retry loop after successful save
                        break  # <-- Exit retry loop here

                    else:
                        print("\nError: Unable to generate a reference number. Form not submitted.")
                        retry = get_yes_no("Would you like to retry submitting the form? (y/n)", "yes")
                        if not retry:
                            print("\nSubmission failed. Returning to the main menu.")
                            break

            elif choice == "2":
                print(Fore.CYAN + "\nEditing an existing report...")
                flt_number = input("Enter the FLT number of the report to edit: ").strip()
                report = load_report(flt_number)
                if report:
                    updated_report = edit_report_field(report)
                    save_to_json(updated_report)
                    insert_into_postgresql(updated_report)
                    print("\nReport updated successfully.")
                else:
                    print("\nReport not found. Returning to the main menu.")

            elif choice == "3":
                print(Fore.RED + "\nThank you for using the Safety Generalist Accident Report Form. Goodbye!")
                break  # Exit the program

            else:
                print(Fore.RED + "Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgram interrupted. Exiting gracefully. Goodbye!")

if __name__ == "__main__":
    main()