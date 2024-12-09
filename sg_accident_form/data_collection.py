# SG Accident Report Data Collection Functions

# Import Libraries and Modules
from .utils import get_yes_no, get_condition, input_with_default, get_date, get_time
from .db_operations import get_or_create_driver, get_or_create_vehicle
from .dot_accident_data import post_accident_testing, post_accident_testing_timeline, dot_recordable, followup_needed, accident_or_incident, citation_info

def person_reporting():
    person_reporting_name = input_with_default("Enter the name of the person or service reporting: ")
    person_reporting_contact = input_with_default("Enter the phone number, email, or source of initial report: ")
    date_reported = get_date("Enter date reported (MM/DD/YYYY): ")
    time_reported = get_time("Enter the time of initial report (HH:MM): ")
    report_completed_by = input_with_default("Enter name of person completing the report: ")
    return {
        "person_reporting_name": person_reporting_name,
        "person_reporting_contact": person_reporting_contact,
        "date_reported": date_reported,
        "time_reported": time_reported,
        "report_completed_by": report_completed_by,
    }
    
def accident_description():
    describe_accident = input_with_default("Briefly describe accident: ")
    return {
        "describe_accident": describe_accident,
    }

def get_driver():
    """
    Collects or retrieves driver details and ensures the driver exists in the database.
    Allows optional skipping of license information and ensures driver creation.
    """
    print("\n--- Enter Driver Details ---")
    # Collect driver details with optional skipping
    driver_name = input("Driver name (Press Enter to skip): ").strip()
    driver_name = driver_name if driver_name else "Unknown"  # Default value if skipped
    driver_phone = input("Driver phone number (Press Enter to skip): ").strip()
    driver_phone = driver_phone if driver_phone else "N/A"  # Default value if skipped
    license_number = input("Driver license number (Press Enter to skip): ").strip()
    license_number = license_number if license_number else None  # Optional field
    license_expiry = get_date("License expiry date (MM/DD/YYYY) (Press Enter to skip): ")
    license_expiry = license_expiry if license_expiry else None  # Optional field
    driver_injury = get_yes_no(f"Is {driver_name} injured? (y/n)") if driver_name != "Unknown" else False

    # Attempt to retrieve or create driver in the database
    driver_id = get_or_create_driver(driver_name, driver_phone, license_number, license_expiry)
    if not driver_id:
        print("Error: Could not retrieve or create driver.")
        return None
    # Return all collected driver details, including database ID
    return {
        "driver_id": driver_id,
        "driver_name": driver_name,
        "driver_phone": driver_phone,
        "license_number": license_number,
        "license_expiry": license_expiry,
        "driver_injury": driver_injury,
    }

def get_vehicle():
    """
    Collects or retrieves vehicle details and ensures the vehicle exists in the database.
    """
    print("\n--- Enter Vehicle Details ---")
    plate_number = input("License plate number: ").strip()
    make = input("Vehicle make (e.g., Toyota, Ford): ").strip()
    model = input("Vehicle model (e.g., Camry, F-150): ").strip()
    year = input("Vehicle year: ").strip()
    vehicle_year = input("Vehicle year (Press Enter to skip): ").strip()
    if not vehicle_year:
        vehicle_year = None  # Allow skipping
    else:
        try:
            vehicle_year = int(vehicle_year)
        except ValueError:
            vehicle_year = None  # Handle invalid input gracefully

    color = input("Vehicle color: ").strip()
    # Use or create vehicle in the database
    vehicle_id = get_or_create_vehicle(plate_number, make, model, year, color)
    if not vehicle_id:
        print("Error: Could not retrieve or create vehicle.")
        return None
    return {
        "vehicle_id": vehicle_id,
        "plate_number": plate_number,
        "make": make,
        "model": model,
        "year": year,
        "color": color,
    }

# Determine Company Details
def get_company_info():
    is_faf = get_yes_no("Is this an FAF (Forward Air) accident? (y/n): ")
    if is_faf:
        faf_branch = get_condition("FAF Branch", ['FAF', 'TQL', 'PLC', 'OMNI'])
        return {"is_faf": True, "faf_branch": faf_branch}
    else:
        return {"is_faf": False, "carrier": input("Enter brokered third-party carrier name: ").strip()}

def get_trailer():
    trailer_connected = get_yes_no("Is a trailer connected? (y/n): ")
    if trailer_connected:
        trailer_type = get_condition("trailer_type", ['Dry Van', 'Refrigerated', 'Bobtail/None'])
        trailer_number = input_with_default("Enter trailer number: ").strip()
        return {
            "trailer_connected": trailer_connected,
            "trailer_type": trailer_type,
            "trailer_number": trailer_number,
        }
    return {"trailer_connected": False}

# --- LOAD INFO --- # 

def load_information():
    manifest_number = input_with_default("Enter manifest number: ", default="Unknown").strip()
    if not manifest_number:
        return {"manifest_number": False}
    
    origin = input_with_default("Enter load origin: ", default="Unknown").strip()
    destination = input_with_default("Enter load destination: ", default="Unknown").strip()

    # Hazmat information
    hazmat = get_yes_no("Hazmat involved? (y/n): ")
    hazmat_description = None
    if hazmat:
        hazmat_description = input_with_default("Describe the hazmat involvement: ", default="Not specified")

    # Service failure information
    service_failure = get_yes_no("Was there a service failure as a result of the accident? (y/n): ")
    extent_of_failure = None
    if service_failure:
        extent_of_failure = input_with_default("If service failure, describe: ", default="Not specified")

    # Freight spillage or damage
    freight_spill_or_damage = get_yes_no("Was there freight spillage or damage as a result of the accident? (y/n): ")

    # Compile and return the collected information
    return {
        "manifest_number": manifest_number,
        "origin": origin,
        "destination": destination,
        "hazmat": hazmat,
        "hazmat_description": hazmat_description if hazmat else None,
        "service_failure": service_failure,
        "extent_of_failure": extent_of_failure if service_failure else None,
        "freight_spill_or_damage": freight_spill_or_damage
    }
    
# ---- 

# # Co-Driver Information
def v1_codriver():
    codriver_present = get_yes_no("Does V1 have a co-driver? (y/n): ")
    if codriver_present:
        codriver_name = input("Enter co-driver name: ").strip()
        codriver_phone = input("Enter co-driver phone number: ").strip()
        codriver_injury = get_yes_no(f"Is {codriver_name} injured? (y/n): ")
        return {
            "codriver_present": codriver_present,
            "codriver_name": codriver_name,
            "codriver_phone": codriver_phone,
            "codriver_injury": codriver_injury,
        }
    return {"codriver_present": False}

# Get V2 Passenger Information
def get_v2_passengers():
    has_passengers = get_yes_no("Does V2 have passengers? (y/n)", "no")
    passengers = []
    if has_passengers:
        num_passengers = input_with_default("How many passengers are there?", "0")
        try:
            num_passengers = int(num_passengers)
        except ValueError:
            num_passengers = 0
        for i in range(num_passengers):
            print(f"Passenger {i + 1}:")
            passenger_name = input_with_default("Enter passenger name", "N/A")
            passenger_injury = get_yes_no(f"Is {passenger_name} injured? (y/n)", "no")
            passengers.append({"name": passenger_name, "injured": passenger_injury})
    return {"has_passengers": has_passengers, "passengers": passengers}

# POLICE INFO
def get_police_information():
    """
    Collects information about police involvement in the accident.
    Returns a dictionary with police-related data.
    """
    police_data = {}
    police_data["police_involvement"] = get_yes_no("Police involved? (y/n): ")
    if police_data["police_involvement"]:
        police_data["police_department"] = input("Enter name of the police department: ").strip()
        police_data["police_officer"] = input("Enter the officer's name: ").strip()
        police_data["police_badge"] = input("Enter the badge number or None: ").strip()
        police_data["police_report"] = input("Enter the police report or case number: ").strip()
    else:
        police_data = {
            "police_involvement": False,
            "police_department": None,
            "police_officer": None,
            "police_badge": None,
            "police_report": None,
        }
    return police_data

# TOW INFO
def get_tow_information():
    """
    Collects information about tow services used in the accident.
    Returns a dictionary with tow-related data.
    """
    tow_data = {}
    tow_data["tow_required"] = get_yes_no("Is a tow service required? (y/n): ")
    if tow_data["tow_required"]:
        tow_data["tow_disabling"] = get_yes_no("Is one or more vehicles disabled? (y/n): ")
        tow_data["tow_company_name"] = input("Enter the tow company's name: ").strip()
        tow_data["tow_company_phone"] = input("Enter the tow company's phone number: ").strip()
        tow_data["tow_company_address"] = input("Enter the tow yard address: ").strip()
    else:
        tow_data = {
            "tow_required": False,
            "tow_disabling": None,
            "tow_company_name": None,
            "tow_company_phone": None,
            "tow_company_address": None,
        }
    return tow_data

# Additional Remarks Section
def get_additional_remarks():
    remarks = input("Enter any additional remarks or observations (Press Enter to skip): ").strip()
    return remarks if remarks else "No additional remarks provided."

def collect_accident_data():
    """
    Orchestrates the collection of all accident-related data.
    Returns a dictionary containing the collected information.
    """
    accident_data = {}
    print("\n--- Incident Information ---")
    # Collect company information
    accident_data["company_info"] = get_company_info()
    # Person / Service Reporting Information
    accident_data["person_reporting"] = person_reporting()
    # Collect accident basics
    accident_data["accident_date"] = get_date("Enter accident date (MM/DD/YYYY): ")
    accident_data["accident_time"] = input_with_default("Enter accident time (HH:MM): ", default="Not specified")
    # Location and Description Info 
    print("\n--- Accident Location and Description Info ---")
    accident_data["accident_location"] = input_with_default("Enter accident location or address: ", default="Not specified")
    accident_data["accident_description"] = accident_description()
    # Load Information
    print("\n--- Load Information ---")
    accident_data["load_info"] = load_information()
    # Police Information
    print("\n--- Law Enforcement Information ---")
    accident_data["police_info"] = get_police_information()   
    # Collect weather and road conditions
    accident_data["weather_info"] = get_condition("weather_conditions", ['Clear', 'Overcast', 'Rainy', 'Windy', 'Snowy'])
    accident_data["road_conditions"] = get_condition("road_conditions", ['Dry', 'Wet', 'Icy', 'Snowy'])
    # DOT Testing
    print("\n DOT Testing")
    accident_data["post_accident_testing"] = post_accident_testing()
    accident_data["post_accident_timeline"] = post_accident_testing_timeline()
    accident_data["dot_recordable"] = dot_recordable()
    accident_data["follow_up"] = followup_needed() or {"followup_needed": False}
    # Collect V1 driver and vehicle information
    print("\n--- V1 Driver Details ---")
    v1_driver = get_driver()
    accident_data["v1_driver"] = v1_driver
    accident_data["driver_id"] = v1_driver.get("driver_id", "Unknown")
    accident_data["v1_citation"] = citation_info()
    accident_data["v1_codriver"] = v1_codriver()
    print("\n--- V1 Vehicle Details ---")
    accident_data["v1_vehicle"] = get_vehicle()
    # Collect Trailer Information
    print("\n--- Trailer Information ---")
    accident_data["trailer_info"] = get_trailer()
    print("\n--- Tow Information ---")
    accident_data["tow_info"] = get_tow_information()
    # Collect V2 driver and vehicle information
    print("\n--- V2 Driver Details ---")
    accident_data["v2_driver"] = get_driver()
    print("\n--- V2 Vehicle Details ---")
    accident_data["v2_vehicle"] = get_vehicle()
    # Additional remarks
    accident_data["additional_remarks"] = get_additional_remarks()
    return accident_data
