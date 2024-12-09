# Import Libraries and Modules
import questionary
from utils import get_condition, get_yes_no, input_with_default 

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

from .utils import get_time, get_date, get_yes_no, input_with_default

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
    
dot_recordable_result = dot_recordable()

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