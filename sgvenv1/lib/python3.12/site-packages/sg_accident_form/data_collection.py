# SG Accident Report Data Collection Functions
# Import Libraries and Modules
from .utils import get_yes_no, get_condition, input_with_default, get_date, get_time
from .db_operations import get_or_create_driver, get_or_create_vehicle
import questionary


def person_reporting():
    person_reporting_name = input_with_default("Enter the name of the person or service reporting: ", "Unknown")
    person_reporting_contact = input_with_default("Enter the phone number, email, or source of initial report: ", "Unknown")
    date_reported = get_date("Enter date reported (MM/DD/YYYY): ")
    time_reported = get_time("Enter the time of initial report (HH:MM): ")
    report_completed_by = input_with_default("Enter name of person completing the report: ", "Unknown")
    return {
        "person_reporting_name": person_reporting_name,
        "person_reporting_contact": person_reporting_contact,
        "date_reported": date_reported,
        "time_reported": time_reported,
        "report_completed_by": report_completed_by,
    }
    
def accident_description():
    describe_accident = input_with_default("Briefly describe accident: ", "None")
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
    driver_name = input_with_default("Driver name (Press Enter to skip): ", "Unknown")
    driver_phone = input_with_default("Driver phone number (Press Enter to skip): ", "N/A")
    license_number = input_with_default("Driver license number (Press Enter to skip): ", None)
    license_expiry = get_date("License expiry date (MM/DD/YYYY) (Press Enter to skip): ")

    # Handle driver injury only if driver_name is known
    driver_injury = get_yes_no(f"Is {driver_name} injured? (y/n)", "no") if driver_name != "Unknown" else False

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
    is_saf = get_yes_no("Is this an SAF (Somewhere Air) accident? (y/n): ")
    if is_saf:
        saf_branch = get_condition("SAF Branch", ['SAF', 'IQT', 'CLP', 'INMO'])
        return {"is_saf": True, "saf_branch": saf_branch}
    else:
        return {"is_saf": False, "carrier": input("Enter brokered third-party carrier name: ").strip()}

def get_trailer():
    trailer_connected = get_yes_no("Is a trailer connected? (y/n): ")
    if trailer_connected:
        trailer_type = get_condition("trailer_type", ['Dry Van', 'Refrigerated', 'Bobtail/None'])
        trailer_number = input_with_default("Enter trailer number: ", "N/A").strip()
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
def post_accident_testing():
    print("\nPost-Accident Alcohol and Drug Testing Criteria")

    fatality = get_yes_no("Was there a fatality as a result of the accident? (y/n): ")
    if fatality:
        print("Testing Required")
        return {"fatality": True, "testing_required": True}

    disabling_tow = get_yes_no("Did any vehicle sustain disabling damage requiring it to be towed? (y/n): ")
    transported_injury = get_yes_no("Was anyone transported for immediate medical treatment away from the scene? (y/n): ")

    if disabling_tow or transported_injury:
        citation = get_yes_no("Was V1 issued a citation? (y/n): ")
        if citation:
            print("Testing Required")
            return {
                "disabling_tow": disabling_tow, 
                "transported_injury": transported_injury, 
                "citation": True, 
                "testing_required": True
            }

    print("No Test Required")
    return {
        "fatality": False,
        "disabling_tow": disabling_tow,
        "transported_injury": transported_injury,
        "citation": False, 
        "testing_required": False
    }
# result = post_accident_testing()
# print(result)

def post_accident_testing_timeline():
    # Steps to initiate the test
    steps_to_initiate_test = input_with_default("Describe steps taken to initiate post-accident testing: ", default="Not specified")
    # Reason if no test can be done
    test_cannot_be_done = input_with_default("If no test can be done, document the reason here: ", default="N/A")
    # Drug test completion status
    drug_test_completed = get_yes_no("Drug Test Completed? (y/n): ")
    # Alcohol test within 2 hours
    bat_within_2_hours = get_yes_no("Was the alcohol test attempted within 2 hours? (y/n): ")
    # Alcohol test completion status
    alcohol_test_completed = get_yes_no("Alcohol Test Completed? (y/n): ")
    # Return a structured dictionary with all responses
    return {
        "steps_to_initiate_test": steps_to_initiate_test,
        "test_cannot_be_done": test_cannot_be_done,
        "drug_test_completed": drug_test_completed,
        "bat_within_2_hours": bat_within_2_hours,
        "alcohol_test_completed": alcohol_test_completed,
    }

def citation_info():
    citation_issued = get_yes_no("Was the driver issued a citation? (y/n): ")
    
    if citation_issued:
        print("\nCollecting citation details...")
        citation_issued_date = get_date("Input date citation was issued (YYYY-MM-DD): ")
        citation_issued_time = get_time("Input time citation was issued (HH:MM): ")
        citation_description = input_with_default("Describe the offense: ", default="Not specified")
        
        return {
            "citation_issued": True,
            "citation_issued_date": citation_issued_date,
            "citation_issued_time": citation_issued_time,
            "citation_description": citation_description,
        }

    # When no citation is issued
    print("No citation issued. Skipping citation details.")
    return {
        "citation_issued": False
    }

def dot_recordable():
    print("\nDOT Recordable Accident Criteria")
    
    cmv_involved = get_yes_no("Did the accident involve a CMV? (y/n): ")
    if cmv_involved:
        return {"cmv_involved": True, "dot_recordable": True}
    
    public_roadway = get_yes_no("Did the accident occur on a roadway open to the public in interstate or intrastate commerce? (y/n): ")
    if public_roadway:
        return{"public_roadway": True, "dot_recordable": True}
    
    fatality = get_yes_no("Did the accident result in a fatality? (y/n): ")
    if fatality:
        return{"fatality": True, "dot_recordable": True}
    
    transported_injury = get_yes_no("Did the accident result in bodily injury to a person who, as a result of the injury, immediately receives medical treatment away from the scene of the accident? (y/n): ")
    if transported_injury:
        return {"transported_injury": True, "dot_recordable": True}
    
    disabling_tow = get_yes_no("Did the accident result in one or more motor vehicles incurring disabling damage that required they be transported away from the scene by a tow truck or other motor vehicle? (y/n): ")
    if disabling_tow:
        return {"disabling_tow": True, "dot_recordable": True}
    
    print("Not DOT Recordable")
    return {
        "cmv_involved": False, 
        "public_roadway": False, 
        "fatality": False, 
        "transported_injury": False, 
        "disabling_tow": False,
        "dot_recordable": False,
    }
    

def followup_needed():
    preventable_accident = get_yes_no("Was the accident preventable? (y/n): ")
    if preventable_accident: 
        print("Follow-up is required for all preventable accidents or incidents.")
        return {"followup_needed": True}

def accident_or_incident():
    print("\nAccident or Incident Classification")

    accident = get_yes_no("Was more than one vehicle involved? (y/n): ")
    if accident:
        return {"accident": True, "incident": False, "claims_only": False}

    incident = get_condition(
        questionary.list(
            choices=[
                "Stationary Object", 
                "Bollard", 
                "Overhead Wires", 
                "Wall", 
                "Unavoidable Road Debris", 
                "Avoidable Road Debris", 
                "Animal Strike"
            ]
        )
    )
    if incident:
        return {"accident": False, "incident": True, "claims_only": False}

    claims_only = get_yes_no("Is this a claims-only case (e.g., minor damage with no vehicle involvement)? (y/n): ")
    return {"accident": False, "incident": False, "claims_only": claims_only}


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
