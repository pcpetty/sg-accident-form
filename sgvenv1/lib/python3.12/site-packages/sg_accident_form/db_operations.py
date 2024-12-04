# SG Database Operations
# ----- SQL DB Integration ----- # 
import psycopg2
from psycopg2.extras import Json
import json
import datetime
from .utils import input_with_default

# Connect to PostgreSQL
def connect_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="accident_reports_db",
            user="safety_generalist",
            password="SierraDecember1997@",
            host="localhost",  # Adjust if using a remote database
            port="5432"        # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Insert Report into PostgreSQL
def insert_into_postgresql(data):
    """
    Inserts the accident report data into the PostgreSQL database.
    Handles serialization for unsupported data types like datetime and sets.
    """
    # Custom serializer for JSON
    def custom_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Type {type(obj)} not serializable")
    conn = connect_postgresql()  # Connect to the PostgreSQL database
    if conn is None:
        print("Failed to connect to PostgreSQL. Data not saved.")
        return
    try:
        with conn.cursor() as cursor:
            print("Attempting to insert data into the database...")
            # Serialize data with custom handling for JSONB
            cursor.execute(
    "INSERT INTO accident_reports (reference_key, report_data) VALUES (%s, %s)",
    [data["reference_key"], Json(data)]
    )
        conn.commit()  # Commit the transaction
        print("Data successfully saved to PostgreSQL.")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
    finally:
        conn.close()  # Always close the connection

# ---- DRIVER ID INTEGRATION ---- #
# Insert or Get Driver ID
def get_or_create_driver(name, phone, license_number, license_expiry):
    """
    Retrieves a driver from the database if they exist, or creates a new one.
    Returns the driver's database ID.
    """
    conn = connect_postgresql()
    if not conn:
        print("Database connection failed.")
        return None

    try:
        with conn.cursor() as cursor:
            # Check if the driver already exists
            cursor.execute(
                """
                SELECT driver_id FROM drivers
                WHERE name = %s AND (phone_number = %s OR phone_number IS NULL)
                """,
                (name, phone),
            )
            result = cursor.fetchone()
            if result:
                return result[0]  # Return existing driver ID

            # Insert a new driver if not found
            cursor.execute(
                """
                INSERT INTO drivers (name, phone_number, license_number, license_expiry)
                VALUES (%s, %s, %s, %s)
                RETURNING driver_id
                """,
                (name, phone, license_number, license_expiry),
            )
            conn.commit()
            return cursor.fetchone()[0]  # Return new driver ID
    except Exception as e:
        print(f"Error in get_or_create_driver: {e}")
        return None
    finally:
        conn.close()

# Insert or Get Vehicle ID
def get_or_create_vehicle(plate_number, make, model, year, color):
    conn = connect_postgresql()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            # Check if vehicle exists
            cursor.execute(
                "SELECT vehicle_id FROM vehicles WHERE plate_number = %s",
                (plate_number,)
            )
            vehicle = cursor.fetchone()
            if vehicle:
                return vehicle[0]

            # Insert new vehicle
            cursor.execute(
                """
                INSERT INTO vehicles (plate_number, make, model, year, color)
                VALUES (%s, %s, %s, %s, %s) RETURNING vehicle_id
                """,
                (plate_number, make, model, year, color)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error handling vehicle data: {e}")
    finally:
        conn.close()
        
# ---- FLT---- #
def get_next_flt_number():
    conn = connect_postgresql()
    if conn is None:
        print("Failed to connect to PostgreSQL for FLT number generation.")
        return None
    try:
        with conn.cursor() as cursor:
            # Retrieve the last number
            cursor.execute("SELECT last_number FROM flt_sequence LIMIT 1;")
            last_number = cursor.fetchone()[0]
            # Increment the number
            next_number = last_number + 1
            # Update the sequence table
            cursor.execute("UPDATE flt_sequence SET last_number = %s;", (next_number,))
            # Commit the change
            conn.commit()
            # Format the number as FLT########
            return f"FLT{next_number:07d}"
    except psycopg2.errors.InsufficientPrivilege as e:
        print(f"Permission error: {e}")
        print("Ensure the user has SELECT and UPDATE privileges on the flt_sequence table.")
        return None
    except Exception as e:
        print(f"Error generating FLT number: {e}")
        return None
    finally:
        conn.close()

# Load a report by FLT number
def load_report(flt_number, filename="accident_report.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        # Find the report by FLT number
        for report in data:
            if report.get("reference_key") == flt_number:
                return report
        print(f"No report found with reference number: {flt_number}")
        return None
    except FileNotFoundError:
        print("No existing reports found.")
        return None

# Edit a specific field in the report
def edit_report_field(report):
    print("\nEditing Report:")
    for key, value in report.items():
        print(f"{key}: {value}")
        new_value = input_with_default(f"Enter new value for {key} or press Enter to keep the current value", value)
        if new_value != value:
            report[key] = new_value
    return report

# ---- ASSET ID INTEGRATION ---- # 
def fetch_driver_name(driver_id):
    """
    Fetches the driver's name from the database using the driver_id.
    """
    conn = connect_postgresql()
    if not conn:
        print("Database connection failed.")
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM drivers WHERE driver_id = %s", (driver_id,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown"
    except Exception as e:
        print(f"Error fetching driver name: {e}")
        return "Unknown"
    finally:
        conn.close()

def fetch_vehicle_plate(vehicle_id):
    """
    Fetches the vehicle's plate from the database using the vehicle_id.
    """
    conn = connect_postgresql()
    if not conn:
        print("Database connection failed.")
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT license_plate FROM vehicles WHERE vehicle_id = %s", (vehicle_id,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown"
    except Exception as e:
        print(f"Error fetching vehicle plate: {e}")
        return "Unknown"
    finally:
        conn.close()
