# RISK RANGER STREAMLIT VERSION # ------------------------------------------------------------------------------------------------
# Import Libraries and Modules # ------------------------------------------------------------------------------------------------
import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import textwrap
from fpdf import FPDF
from colorama import init, Fore, Style
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import json
from openpyxl.chart import BarChart, Reference
from pathlib import Path
# ------------------------------------------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES # ------------------------------------------------------------------------------------------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# ------------------------------------------------------------------------------------------------
# CONNECT TO PSQL DB # ------------------------------------------------------------------------------------------------
def connect_db():
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None
# ------------------------------------------------------------------------------------------------
# GET DATA FROM PSQL # ------------------------------------------------------------------------------------------------
def fetch_data(query, params=None):
    """
    Executes a query and fetches data from the database.
    """
    engine = connect_db()
    if engine:
        try:
            with engine.connect() as conn:
                return pd.read_sql_query(query, conn, params=params)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()
# ------------------------------------------------------------------------------------------------
# SAVE DATA FUNCTION # ------------------------------------------------------------------------------------------------
def save_data(query, params):
    """
    Saves data to the database.
    """
    engine = connect_db()
    if engine:
        try:
            with engine.connect() as conn:
                conn.execute(query, params)
                st.success("Data saved successfully!")
        except Exception as e:
            st.error(f"Failed to save data: {e}")
# ------------------------------------------------------------------------------------------------
# LOGO FUNCTION # -------------------------------------------------------------------------------------
def display_logo():
    st.image("RRLOGOBANNER.png")
# LOGO SIDEBAR # ------------------------------------------------------------------------------------------------
# Add a smaller logo to the sidebar
st.sidebar.image(
    "RRLOGOSMALL.png")
# LOGO FOOTER # --------------------------------------------------------------------------------------------------
# Add a banner at the footer
st.markdown(
    """
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; background-color: black; color: orange; padding: 10px;'>
        <h4>RiskRanger | Logistics Simplified</h4>
    </div>
    """,
    unsafe_allow_html=True
)
# ------------------------------------------------------------------------------------------------
# TUTORIAL FUNCTION # ------------------------------------------------------------------------------------------------
def tutorial():
    """
    Provides a step-by-step accident reporting tutorial.
    """
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
    st.header("Accident Reporting SOP Tutorial")
    # for i, step in enumerate(steps, start=1):
    #     st.markdown(f"**{i}. {step}**")
    #     if i < len(steps) and not st.button(f"Next Step {i+1}", key=f"step_{i}"):
    #         break
    # else:
    #     st.success("Tutorial Complete!")
# ------------------------------------------------------------------------------------------------
# PROGRAM LOGIC FUNCTIONS AND UTILITY #-------------------------------------------------------------------------------------------------------
def get_yes_no(prompt):
    """
    Displays a yes or no question in Streamlit and returns a boolean response.
    Args:
        prompt (str): The question to display.
    Returns:
        bool: True if "Yes" is selected, False if "No" is selected.
    """
    response = st.radio(prompt, options=["Yes", "No"], index=1)  # Default to "No"
    return response == "Yes"

# ------------------------------------------------------------------------------------------------
# INPUT WITH DEFAULT FUNCTION # ------------------------------------------------------------------------------------------------
def text_input_with_default(label, default_value=""):
    """
    Handles text input with a default value in Streamlit.
    """
    # Correctly call st.text_input here
    input_value = st.text_input(label, value=default_value)
    # Strip whitespace from the input
    return input_value.strip()
# ------------------------------------------------------------------------------------------------
# NUMERIC INPUT WITH DEFAULT FUNCTION ------------------------------------------------------------------------------------------------
def numeric_input_with_default(label, default_value=0):
    return numeric_input_with_default(label, value=default_value)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCIDENT REPORT DATA COLLECTION FUNCTIONS # ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# PERSON REPORTING FUNCTION # ------------------------------------------------------------------------------------------------
def person_reporting():
    st.subheader("Incident Information")
    person_reporting_name = text_input_with_default("Enter the name of the person or service reporting:")
    person_reporting_contact = text_input_with_default("Enter the phone number, email, or source of initial report:")
    date_reported = st.date_input("Enter date reported (MM/DD/YYYY): ")
    time_reported = st.time_input("Enter the time of initial report (HH:MM): ")
    report_completed_by = text_input_with_default("Enter name of person completing the report:")
    return {
        "person_reporting_name": person_reporting_name,
        "person_reporting_contact": person_reporting_contact,
        "date_reported": date_reported,
        "time_reported": time_reported,
        "report_completed_by": report_completed_by,
    }
# ------------------------------------------------------------------------------------------------
# LOAD INFO FUNCTION # ------------------------------------------------------------------------------------------------
# LOAD INFO FUNCTION # ------------------------------------------------------------------------------------------------
def load_information():
    """
    Collects load-specific information for the accident report.
    """
    st.subheader("Load Information")
    # Basic load details
    manifest_number = text_input_with_default("Manifest Number:")
    origin = text_input_with_default("Load Origin:")
    destination = text_input_with_default("Load Destination:")
    # Hazardous material details
    hazmat = get_yes_no("Does this involve hazardous materials (HAZMAT)? (y/n):")
    hazmat_description = None
    if hazmat:
        hazmat_description = text_input_with_default("Provide a brief description of the hazmat situation:", default_value="N/A")
    # Load failure details
    failure = get_yes_no("Did the load fail in any way? (y/n):")
    extent_of_failure = None
    if failure:
        extent_of_failure = text_input_with_default("Describe the extent of the failure:", default_value="N/A")
    # Freight spill or damage
    freight_spill_or_damage = get_yes_no("Was there freight spillage or damage as a result of the accident? (y/n):")
    # Additional load information
    load_weight = st.number_input("Enter load weight (in lbs):", min_value=0, value=0)
    load_type = st.selectbox("Select load type:", ["General Freight", "Household Goods", "Chemicals", "Other"])
    # Return structured data
    return {
        "manifest_number": manifest_number,
        "origin": origin,
        "destination": destination,
        "hazmat": hazmat,
        "hazmat_description": hazmat_description,
        "load_weight": load_weight,
        "load_type": load_type,
        "service_failure": failure,
        "extent_of_failure": extent_of_failure,
        "freight_spill_or_damage": freight_spill_or_damage
    }
# ------------------------------------------------------------------------------------------------
# TOW INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_tow_information():
    """
    Collects information about tow services using Streamlit.
    Returns a dictionary with tow-related data.
    """
    st.subheader("Tow Information")
    tow_data = {}
    
    tow_required = get_yes_no("Is a tow service required?")
    tow_data["tow_required"] = tow_required == "Yes"
    
    if tow_data["tow_required"]:
        tow_disabling = get_yes_no("Is one or more vehicles disabled?")
        tow_data["tow_disabling"] = tow_disabling == "Yes"
        tow_data["tow_company_name"] = text_input_with_default("Enter the tow company's name:")
        tow_data["tow_company_phone"] = text_input_with_default("Enter the tow company's phone number:")
        tow_data["tow_company_address"] = st.text_area("Enter the tow yard address:")
    else:
        tow_data.update({
            "tow_disabling": None,
            "tow_company_name": None,
            "tow_company_phone": None,
            "tow_company_address": None,
        })
        
    return tow_data
# ------------------------------------------------------------------------------------------------
# POLICE INFORMATION FUNCTION # ------------------------------------------------------------------------------------------------
def get_police_information():
    """
    Collects information about police involvement in the accident.
    Returns a dictionary with police-related data.
    """
    st.subheader("Police Information")
    police_data = {}
    
    police_involvement = get_yes_no("Police involved?:")
    police_data["police_involvement"] = police_involvement == "Yes"
    
    if police_data["police_involvement"]:
        police_involvement["police_department"] = text_input_with_default("Enter name of the police department:")
        police_involvement["police_officer"] = text_input_with_default("Enter the officer's name:")
        police_involvement["police_badge"] = text_input_with_default("Enter the badge number or None:")
        police_involvement["police_report"] = text_input_with_default("Enter the police report or case number:")
    else:
        police_data.update({
            "police_involvement": None,
            "police_department": None,
            "police_officer": None,
            "police_badge": None,
            "police_report": None,
        })
        
    return police_data
# ------------------------------------------------------------------------------------------------
# GET OR CREATE DRIVER FUNCTION - DB OPERATIONS # ----------------------------------------------------------------------------
def get_or_create_driver(name, phone, license_number, license_expiry):
    """
    Retrieves a driver from the database if they exist, or creates a new one.
    Returns the driver's database ID.
    """
    engine = connect_db()
    if not engine:
        st.error("Database connection failed.")
        return None
    try:
        with engine.connect() as conn:
            # Check if the driver already exists
            query_check = """
            SELECT driver_id FROM drivers
            WHERE name = :name AND (phone_number = :phone OR phone_number IS NULL)
            """
            result = conn.execute(query_check, {"name": name, "phone": phone}).fetchone()
            if result:
                st.info("Driver found in database.")
                return result[0]  # Return existing driver ID
            # Insert a new driver if not found
            query_insert = """
            INSERT INTO drivers (name, phone_number, license_number, license_expiry)
            VALUES (:name, :phone, :license_number, :license_expiry)
            RETURNING driver_id
            """
            result = conn.execute(query_insert, {
                "name": name,
                "phone": phone,
                "license_number": license_number,
                "license_expiry": license_expiry,
            }).fetchone()
            st.success("New driver created successfully.")
            return result[0]  # Return new driver ID
    except Exception as e:
        st.error(f"Error in get_or_create_driver: {e}")
        return None
# ------------------------------------------------------------------------------------------------        
# V1 DRIVER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_driver():
    """
    Collects or retrieves driver details and ensures the driver exists in the database.
    Allows optional skipping of license information and ensures driver creation.
    """
    st.subheader("Enter Driver Details")
    
    # Collect driver details
    driver_name = text_input_with_default("Driver name:", value="Unknown")
    driver_phone = text_input_with_default("Driver phone number (Optional):", value="N/A")
    license_number = numeric_input_with_default("Driver license number (Optional):", value="")
    license_expiry = st.date_input("License expiry date (Optional):", value=None)
    
    # Handle driver injury only if driver_name is known
    if driver_name != "Unknown":
        driver_injury = st.radio(f"Is {driver_name} injured?", options=["Yes", "No"], index=1)
        driver_injury = driver_injury == "Yes"
    else:
        driver_injury = False
        
    # Placeholder for database interaction
    driver_id = get_or_create_driver(driver_name, driver_phone, license_number, license_expiry)
    
    if not driver_id:
        st.error("Error: Could not retrieve or create driver.")
        return None
    
    # Return all collected driver details
    return {
        "driver_id": driver_id,
        "driver_name": driver_name,
        "driver_phone": driver_phone,
        "license_number": license_number,
        "license_expiry": license_expiry,
        "driver_injury": driver_injury,
    }
# ------------------------------------------------------------------------------------------------    
# GET OR CREATE VEHICLE FUNCTION - DB OPS # ------------------------------------------------------------------------------------------------  
def get_or_create_vehicle(plate_number, make, model, year, color):
    """
    Retrieves a vehicle from the database if it exists or creates a new one.
    Returns the vehicle's database ID.
    """
    engine = connect_db()
    if not engine:
        st.error("Database connection failed.")
        return None
    try:
        with engine.connect() as conn:
            # Check if the vehicle already exists
            query_check = """
            SELECT vehicle_id FROM vehicles
            WHERE plate_number = :plate_number
            """
            result = conn.execute(query_check, {"plate_number": plate_number}).fetchone()
            if result:
                return result[0]  # Return existing vehicle ID
            # Insert a new vehicle if not found
            query_insert = """
            INSERT INTO vehicles (plate_number, make, model, year, color)
            VALUES (:plate_number, :make, :model, :year, :color)
            RETURNING vehicle_id
            """
            result = conn.execute(query_insert, {
                "plate_number": plate_number,
                "make": make,
                "model": model,
                "year": year,
                "color": color
            }).fetchone()
            return result[0]  # Return new vehicle ID
    except Exception as e:
        st.error(f"Error in get_or_create_vehicle: {e}")
        return None
# ------------------------------------------------------------------------------------------------
# V1 VEHICLE INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_vehicle():
    """
    Collects or retrieves vehicle details and ensures the vehicle exists in the database.
    """
    st.subheader("Vehicle Information")
    
    # Collect vehicle details
    plate_number = st.text_input("License plate number:", placeholder="Enter license plate number")
    make = st.text_input("Vehicle make:", placeholder="Enter vehicle make")
    model = st.text_input("Vehicle model:", placeholder="Enter vehicle model")
    year = st.number_input("Vehicle year:", min_value=1900, max_value=2100, step=1, format="%d")
    color = st.text_input("Vehicle color:", placeholder="Enter vehicle color")
    
    # Attempt to retrieve or create the vehicle in the database
    vehicle_id = get_or_create_vehicle(plate_number, make, model, year, color)
    if not vehicle_id:
        st.error("Error: Could not retrieve or create vehicle.")
        return None
    
    # Return collected and processed vehicle details
    return {
        "vehicle_id": vehicle_id,
        "plate_number": plate_number,
        "make": make,
        "model": model,
        "year": int(year) if year else None,
        "color": color,
    }
# ------------------------------------------------------------------------------------------------
# COMPANY DETAILS FUNCTION # ------------------------------------------------------------------------------------------------
def get_company_info():
    st.subheader("Company or Division")
    is_saf = get_yes_no("Is this an SAF (Somewhere Air) accident? (y/n): ")
    if is_saf:
        saf_branch = st.selectbox("Company Division:", ["SAF", "IQT", "CLP", "INMO"])
        return {"is_saf": True, "saf_branch": saf_branch}
    else:
        return {"is_saf": False, "carrier": st.text_input("Enter brokered third-party carrier name: ").strip()}
# ------------------------------------------------------------------------------------------------
# TRAILER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_trailer() -> dict:
    """
    Collects information about the trailer if connected.
    Returns:
        dict: A dictionary containing trailer connection status and details if connected.
    """
    st.subheader("Trailer Information")
    trailer_connected = get_yes_no("Is a trailer connected? (y/n): ")
    if trailer_connected:
        trailer_type = st.selectbox("Trailer Type", ['Dry Van', 'Refrigerated', 'Bobtail/None'])
        trailer_number = text_input_with_default("Enter the trailer number: ", value="N/A").upper().strip()
        
        # Validation
        if not trailer_number:
            st.warning("Trailer number cannot be empty!")
            return {"trailer_connected": trailer_connected}
        
        return {
            "trailer_connected": trailer_connected,
            "trailer_type": trailer_type,
            "trailer_number": trailer_number,
        }
    return {"trailer_connected": False}
# --------------------------------------------------------------------------------------------------
# POST-ACCIDENT-TESTING FUNCTION # ------------------------------------------------------------------------------------------------
def post_accident_testing():
    """
    Evaluates the need for post-accident alcohol and drug testing based on regulatory criteria.
    """
    st.subheader("Post-Accident Alcohol and Drug Testing Criteria")
    # Check for fatality
    fatality = get_yes_no("Was there a fatality as a result of the accident? (y/n): ")
    if fatality:
        st.success("Testing Required due to a fatality.")
        return {"fatality": True, "testing_required": True}
    # Check for disabling tow or transported injury
    disabling_tow = get_yes_no("Did any vehicle sustain disabling damage requiring it to be towed? (y/n): ")
    transported_injury = get_yes_no("Was anyone transported for immediate medical treatment away from the scene? (y/n): ")
    # If disabling tow or transported injury, check for citation
    if disabling_tow or transported_injury:
        citation = get_yes_no("Was V1 issued a citation? (y/n): ")
        if citation:
            st.success("Testing Required due to disabling tow or transported injury with citation.")
            return {
                "fatality": False,
                "disabling_tow": disabling_tow,
                "transported_injury": transported_injury,
                "citation": True,
                "testing_required": True
            }
    # No testing required
    st.info("No Testing Required.")
    return {
        "fatality": False,
        "disabling_tow": disabling_tow,
        "transported_injury": transported_injury,
        "citation": False,
        "testing_required": False
    }
# ------------------------------------------------------------------------------------------------
# POST-ACCIDENT-TESTING TIMELINE FUNCTION # ------------------------------------------------------------------------------------------------
def post_accident_testing_timeline():
    """
    Collects details about the post-accident testing timeline and status.
    Returns a structured dictionary of user inputs.
    """
    st.subheader("Post-Accident Testing Timeline")
    # Steps to initiate the test
    steps_to_initiate_test = text_input_with_default(
        "Describe steps taken to initiate post-accident testing:", 
        default_value="Not specified"
    )
    # Reason if no test can be done
    test_cannot_be_done = text_input_with_default(
        "If no test can be done, document the reason here:", 
        default_value="N/A"
    )
    # Drug test completion status
    drug_test_completed = get_yes_no("Was the drug test completed?")
    # Alcohol test within 2 hours
    bat_within_2_hours = get_yes_no("Was the alcohol test attempted within 2 hours?")
    # Alcohol test completion status
    alcohol_test_completed = get_yes_no("Was the alcohol test completed?")
    # Return structured dictionary with all responses
    result = {
        "steps_to_initiate_test": steps_to_initiate_test,
        "test_cannot_be_done": test_cannot_be_done,
        "drug_test_completed": drug_test_completed,
        "bat_within_2_hours": bat_within_2_hours,
        "alcohol_test_completed": alcohol_test_completed,
    }
    # Display the summary for user review
    st.subheader("Summary of Post-Accident Testing Timeline")
    st.json(result)  # Nicely formatted display of the dictionary
    return result
# ------------------------------------------------------------------------------------------------
# CITATION FUNCTION # ------------------------------------------------------------------------------------------------
def citation_info():
    """
    Collects details about a citation issued during the accident.
    Returns a dictionary containing citation-related information.
    """
    st.subheader("Citation Information")
    
    # Check if a citation was issued
    citation_issued = get_yes_no("Was the driver issued a citation?")
    
    if citation_issued:
        st.info("Collecting citation details...")
        
        # Collect citation details
        citation_issued_date = st.date_input("Input date citation was issued (YYYY-MM-DD):", key="citation_date")
        citation_issued_time = st.time_input("Input time citation was issued (HH:MM):", key="citation_time")
        citation_description = text_input_with_default("Describe the offense:", default_value="Not specified")
        
        # Return the collected data
        return {
            "citation_issued": True,
            "citation_issued_date": citation_issued_date,
            "citation_issued_time": citation_issued_time,
            "citation_description": citation_description,
        }
        
    # When no citation is issued
    st.info("No citation issued. Skipping citation details.")
    return {
        "citation_issued": False
    }
# ------------------------------------------------------------------------------------------------
# DOT RECORDABLE FUNCTION # ------------------------------------------------------------------------------------------------
def dot_recordable():
    """
    Evaluates whether an accident meets the criteria for being DOT recordable.
    """
    st.subheader("DOT Recordable Accident Criteria")
    
    # Initialize result dictionary
    result = {
        "cmv_involved": False,
        "public_roadway": False,
        "fatality": False,
        "transported_injury": False,
        "disabling_tow": False,
        "dot_recordable": False
    }
    # Check if a CMV was involved
    result["cmv_involved"] = get_yes_no("Did the accident involve a CMV? (y/n): ")
    if result["cmv_involved"]:
        result["dot_recordable"] = True
        st.success("This accident is DOT recordable because it involved a CMV.")
        return result
    # Check if the accident occurred on a public roadway
    result["public_roadway"] = get_yes_no("Did the accident occur on a public roadway in interstate or intrastate commerce? (y/n): ")
    if result["public_roadway"]:
        result["dot_recordable"] = True
        st.success("This accident is DOT recordable because it occurred on a public roadway.")
        return result
    # Check for fatalities
    result["fatality"] = get_yes_no("Did the accident result in a fatality?:")
    if result["fatality"]:
        result["dot_recordable"] = True
        st.success("This accident is DOT recordable because it resulted in a fatality.")
        return result
    # Check for injuries requiring medical transport
    result["transported_injury"] = get_yes_no("Did the accident result in bodily injury requiring immediate medical treatment away from the scene?:")
    if result["transported_injury"]:
        result["dot_recordable"] = True
        st.success("This accident is DOT recordable because of a transported injury.")
        return result
    # Check for disabling tow
    result["disabling_tow"] = get_yes_no("Did the accident involve disabling damage requiring a tow?:")
    if result["disabling_tow"]:
        result["dot_recordable"] = True
        st.success("This accident is DOT recordable because it involved a disabling tow.")
        return result
    # Not DOT recordable
    st.info("This accident does not meet the criteria for being DOT recordable.")
    return result
# ------------------------------------------------------------------------------------------------
# FOLLOW-UP FUNCTION # ------------------------------------------------------------------------------------------------
def followup_needed():
    """
    Determines whether follow-up actions are required based on the preventability of the event.
    """
    st.subheader("Follow-Up Required?")
    
    # Check if the accident or incident was preventable
    preventable_accident = get_yes_no("Was the accident preventable?:")
    
    if preventable_accident:
        st.warning("Follow-up is required for all preventable accidents or incidents.")
        return {"followup_needed": True, "preventable": True}
    else:
        st.success("No follow-up is required for non-preventable accidents or incidents.")
        return {"followup_needed": False, "preventable": False}
# ------------------------------------------------------------------------------------------------
# ACCIDENT OR INCIDENT FUNCTION # ------------------------------------------------------------------------------------------------
def accident_or_incident():
    """
    Determines whether the event is classified as an accident, incident, or claims-only case.
    """
    st.subheader("Accident or Incident Classification")
    # Determine if it is an accident
    accident = get_yes_no("Was more than one vehicle involved?:")
    if accident:
        st.success("Event classified as an accident.")
        return {"accident": True, "incident": False, "claims_only": False}
    # If not an accident, determine the type of incident
    incident_type = st.selectbox(
        "Select the type of incident:",
        options=[
            "Stationary Object", 
            "Bollard", 
            "Overhead Wires", 
            "Wall", 
            "Unavoidable Road Debris", 
            "Avoidable Road Debris", 
            "Animal Strike"c
        ],
        index=0  # Default selection
    )
    if incident_type:
        st.success(f"Event classified as an incident: {incident_type}.")
        return {"accident": False, "incident": True, "claims_only": False, "incident_type": incident_type}
    # If not an incident, check for claims-only cases
    claims_only = get_yes_no("Is this a claims-only case (e.g., minor damage with no vehicle involvement)?:")
    if claims_only:
        st.success("Event classified as claims-only.")
    else:
        st.info("No classification was made.")
    return {"accident": False, "incident": False, "claims_only": claims_only}
# ------------------------------------------------------------------------------------------------
# CO DRIVER FUNCTION # ------------------------------------------------------------------------------------------------
def v1_codriver():
    codriver_present = get_yes_no("Does V1 have a co-driver?:")
    if codriver_present:
        codriver_name = text_input_with_default("Enter co-driver name:").strip()
        codriver_phone = text_input_with_default("Enter co-driver phone number:").strip()
        codriver_injury = get_yes_no(f"Is {codriver_name} injured?:")
        return {
            "codriver_present": codriver_present,
            "codriver_name": codriver_name,
            "codriver_phone": codriver_phone,
            "codriver_injury": codriver_injury,
        }
    return {"codriver_present": False}
# ------------------------------------------------------------------------------------------------
# V@ PASSENGER INFO FUNCTION # ------------------------------------------------------------------------------------------------
def get_v2_passengers():
    st.subheader("V2 Passenger Info")
    has_passengers = get_yes_no("Does V2 have passengers?:", default="no")
    passengers = []
    if has_passengers:
        num_passengers = text_input_with_default("How many passengers are there?", default="0")
        try:
            num_passengers = numeric_input_with_default(num_passengers)
        except ValueError:
            num_passengers = 0
        for i in range(num_passengers):
            st.text(f"Passenger {i + 1}:")
            passenger_name = text_input_with_default("Enter passenger name", default_value="N/A")
            passenger_injury = get_yes_no(f"Is {passenger_name} injured? (y/n)", default_value="no")
            passengers.append({"name": passenger_name, "injured": passenger_injury})
    return {"has_passengers": has_passengers, "passengers": passengers}
# ------------------------------------------------------------------------------------------------
# ADDITIONAL REMARKS FUNCTION # ------------------------------------------------------------------------------------------------
def get_additional_remarks():
    st.subheader("Additional Remarks")
    remarks = text_input_with_default("Enter any additional remarks or observations:").strip()
    return remarks if remarks else "No additional remarks provided."
# ------------------------------------------------------------------------------------------------
# USER ACCIDENT FORM # ------------------------------------------------------------------------------------------------
def accident_form():
    """
    Displays the accident report form.
    """
    st.header("Accident Information")
    company_info = text_input_with_default("Company Info:", default_value="N/A")
    person_reporting = text_input_with_default("Person Reporting:", default_value="N/A")
    accident_date = st.date_input("Accident Date:")
    accident_time = st.time_input("Accident Time:")
    accident_location = text_input_with_default("Accident Location or Address:", default_value="Unknown")
    accident_description = text_input_with_default("Accident Description:", default_value="Not specified")

    weather_info = st.selectbox("Weather Conditions:", ['Clear', 'Overcast', 'Rainy', 'Windy', 'Snowy'])
    road_conditions = st.selectbox("Road Conditions:", ['Dry', 'Wet', 'Icy', 'Snowy'])

    v1_driver = text_input_with_default("V1 Driver Name:", default_value="Unknown")
    v1_vehicle = text_input_with_default("V1 Vehicle ID or License Plate:", default_value="N/A")

    v2_driver = text_input_with_default("V2 Driver Name:", default_value="Unknown")
    v2_vehicle = text_input_with_default("V2 Vehicle ID or License Plate:", default_value="N/A")

    return {
        "company_info": company_info,
        "person_reporting": person_reporting,
        "accident_date": accident_date,
        "accident_time": accident_time,
        "accident_location": accident_location,
        "accident_description": accident_description,
        "weather_info": weather_info,
        "road_conditions": road_conditions,
        "v1_driver": v1_driver,
        "v1_vehicle": v1_vehicle,
        "v2_driver": v2_driver,
        "v2_vehicle": v2_vehicle
    }

# ------------------------------------------------------------------------------------------------
# DRIVER LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def driver_lookup():
    """
    Provides a UI for looking up driver information.
    """
    st.subheader("Driver Lookup")
    driver_id = text_input_with_default("Enter Driver ID or Name:")
    
    if st.button("Search Driver"):
        query = """
        SELECT * FROM drivers 
        WHERE driver_id = %s OR driver_name ILIKE %s
        """
        params = (driver_id, f"%{driver_id}%")
        driver_data = fetch_data(query, params)
        
        if not driver_data.empty:
            st.write(driver_data)
        else:
            st.warning("No driver found!")
# ------------------------------------------------------------------------------------------------
# VEHICLE LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def vehicle_lookup():
    """
    Provides a UI for looking up vehicle information.
    """
    st.subheader("Vehicle Lookup")
    vehicle_id = text_input_with_default("Enter Vehicle ID or License Plate:")
    
    if st.button("Search Vehicle"):
        query = """
        SELECT * FROM vehicles 
        WHERE vehicle_id = %s OR license_plate ILIKE %s
        """
        params = (vehicle_id, f"%{vehicle_id}%")
        vehicle_data = fetch_data(query, params)
        
        if not vehicle_data.empty:
            st.write(vehicle_data)
        else:
            st.warning("No vehicle found!")
# ------------------------------------------------------------------------------------------------
# CLAIM NUMBER LOOKUP PAGE # ------------------------------------------------------------------------------------------------
def flt_lookup():
    st.subheader("FLT Number Lookup")
    flt_number = numeric_input_with_default("Enter FLT Number:")
    if st.button("Search by FLT"):
        query = """
        SELECT * FROM accident_reports 
        WHERE reference_key = %s
        """
        params = (flt_number,)
        flt_data = fetch_data(query, params)
        if not flt_data.empty:
            st.write(flt_data)
        else:
            st.warning("No records found for this FLT number.")
# ------------------------------------------------------------------------------------------------
# MAIN FUNCTION FOR PROGRAM # ------------------------------------------------------------------------------------------------
def main():
    """
    Main function to render the Streamlit app.
    """
    display_logo()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Accident Report Form", "Driver Lookup", "Vehicle Lookup", "Tutorial", "FLT Lookup"],
    )
    if page == "Home":
        st.title("Welcome to RiskRanger")
        st.write("Your safety management companion.")
    elif page == "Accident Report Form":
        st.title("Accident Report Form")
        # Collect data from various sections
        accident_data = accident_form()
        tow_data = get_tow_information()
        load_info = load_information()
        police_info = get_police_information()
        vehicle1 = get_vehicle()
        driver1 = get_driver()
        reporting_persons = person_reporting()
        classification = accident_or_incident()
        dot_result = dot_recordable()
        testing_result = post_accident_testing()
        followup_info = followup_needed()
        # Display gathered information
        st.write("Classification Result:", classification)
        st.write("Follow-Up Information:", followup_info)
        if dot_result["dot_recordable"]:
            st.write("DOT Recordable Accident Details:", dot_result)
        else:
            st.write("This accident is not DOT recordable.")
        if testing_result["testing_required"]:
            st.write("Testing Details:", testing_result)
        else:
            st.write("No testing required based on the criteria.")
        # Optional Sections
        if st.button("Start Post-Accident Testing Timeline"):
            timeline_data = post_accident_testing_timeline()
            st.write("Timeline Data Submitted:", timeline_data)
        if st.button("Add Citation Information"):
            citation_data = citation_info()
            st.write("Citation Data Collected:", citation_data)
        # Submit Data
        if st.button("Submit Accident Report"):
            st.write("Name of Person Reporting:", reporting_persons)
            st.write("Tow Information:", tow_data)
            st.write("Load Information:", load_info)
            st.write("Police Information:", police_info)
            st.write("Vehicle 1 Info:", vehicle1)
            st.write("Driver 1 Info:", driver1)
            st.write("Accident Classification:", classification)
            
            query = """
            INSERT INTO accident_reports (
                company_info, person_reporting, accident_date, accident_time,
                accident_location, accident_description, weather_info, road_conditions,
                v1_driver, v1_vehicle, v2_driver, v2_vehicle
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                accident_data["company_info"], accident_data["person_reporting"],
                accident_data["accident_date"].strftime('%Y-%m-%d'),
                accident_data["accident_time"].strftime('%H:%M:%S'),
                accident_data["accident_location"], accident_data["accident_description"],
                accident_data["weather_info"], accident_data["road_conditions"],
                accident_data["v1_driver"], accident_data["v1_vehicle"],
                accident_data["v2_driver"], accident_data["v2_vehicle"]
            )
            save_data(query, params)
            
    elif page == "Driver Lookup":
        driver_lookup()
    elif page == "Vehicle Lookup":
        vehicle_lookup()
    elif page == "FLT Lookup":
        flt_lookup()  # Ensure this function is implemented
    elif page == "Tutorial":
        tutorial()
        
if __name__ == "__main__":
    main()
# ------------------------------------------------------------------------------------------------