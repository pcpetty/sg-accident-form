from .data_collection import collect_accident_data
from .db_operations import connect_postgresql, insert_into_postgresql, get_next_flt_number, load_report, edit_report_field
from .report_generation import export_to_excel, export_to_pdf, save_to_json
from .utils import get_yes_no, input_with_default


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

def main():
    try:
        print("Safety Generalist Accident Report Form")

        while True:  # Main menu loop
            print("\nOptions:")
            print("1. Create a new report")
            print("2. Edit an existing report")
            print("3. Exit")

            choice = input_with_default("Choose an option (1/2/3)", "3")

            if choice == "1":
                # Optional SOP Tutorial
                if get_yes_no("Would you like an accident reporting SOP tutorial? (y/n)", "no"):
                    tutorial()

                # Collect new accident data
                accident_data = collect_accident_data()

                # Retry mechanism for FLT number generation and submission
                while True:
                    reference_key = get_next_flt_number()
                    if reference_key:
                        accident_data["reference_key"] = reference_key

                        # Save data
                        save_to_json(accident_data)
                        insert_into_postgresql(accident_data)
                        export_to_excel(accident_data, filename=f"{reference_key}.xlsx")
                        export_to_pdf(accident_data, filename=f"{reference_key}.pdf")

                        print("\nForm Submitted Successfully!")
                        print(f"Your reference number is: {reference_key}")
                        print("Please save this number for future reference.")
                        break  # Exit retry loop
                    else:
                        print("\nError: Unable to generate a reference number. Form not submitted.")
                        retry = get_yes_no("Would you like to retry submitting the form? (y/n)", "yes")
                        if not retry:
                            print("\nSubmission failed. Returning to the main menu.")
                            break

            elif choice == "2":
                # Edit existing report
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
                print("\nThank you for using the Safety Generalist Accident Report Form. Goodbye!")
                break  # Exit the program

            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting gracefully. Goodbye!")

if __name__ == "__main__":
    main()
