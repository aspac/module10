# -----------------------------------------------------------------------------
# wmata_api.py
# -----------------------------------------------------------------------------
# Author: Antonio Spaccavento
# Description:
#   Flask-based microservice that serves as a wrapper around the WMATA
#   ElevatorIncidents API. The service filters incidents by "unit type"
#   (elevators or escalators) and returns a JSON-formatted string.
# -----------------------------------------------------------------------------

import json          # Converts Python objects to JSON text
import requests      # Used to call the external WMATA API
from flask import Flask   # Flask web framework (allowed import)

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
WMATA_API_KEY = "d8eb540b9f894779bfa41cf29206db57"  # Your WMATA API key
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"  # WMATA endpoint

# API header containing your key for authentication
headers = {"api_key": WMATA_API_KEY, "Accept": "*/*"}

# -----------------------------------------------------------------------------
# FLASK APP INITIALIZATION
# -----------------------------------------------------------------------------
app = Flask(__name__)  # Create Flask application instance

# -----------------------------------------------------------------------------
# ROUTE DEFINITION
# -----------------------------------------------------------------------------
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    """
    Endpoint: /incidents/<unit_type>
    Purpose:
        Acts as a wrapper around the WMATA ElevatorIncidents API,
        filtering the results to include only elevator or escalator incidents.
    Parameters:
        unit_type (str): "elevators" or "escalators"
    Returns:
        JSON string of filtered results.
    """

    # Normalize unit_type for comparison
    unit_type = unit_type.lower()

    # Create an empty list to hold incident dictionaries
    incidents = []

    # -------------------------------------------------------------------------
    # STEP 1: Retrieve Data from WMATA API
    # -------------------------------------------------------------------------
    # Perform an HTTP GET request using the requests library
    response = requests.get(INCIDENTS_URL, headers=headers)

    # -------------------------------------------------------------------------
    # STEP 2: Validate API Response
    # -------------------------------------------------------------------------
    if response.status_code == 200:
        # Convert the JSON response text into a Python dictionary
        data = response.json()

        # Extract the list of elevator/escalator incidents
        all_incidents = data.get("ElevatorIncidents", [])

        # ---------------------------------------------------------------------
        # STEP 3: Filter Based on Unit Type
        # ---------------------------------------------------------------------
        for incident in all_incidents:
            # Retrieve and normalize the unit type from each incident record
            api_unit_type = incident.get("UnitType", "").lower()

            # Match "elevator" or "escalator" to user-provided unit_type
            if (unit_type == "elevators" and api_unit_type == "elevator") or \
               (unit_type == "escalators" and api_unit_type == "escalator"):

                # Build a simplified dictionary following Module 7 schema
                incident_obj = {
                    "StationCode": incident.get("StationCode", ""),
                    "StationName": incident.get("StationName", ""),
                    "UnitName": incident.get("UnitName", ""),
                    "UnitType": incident.get("UnitType", "")
                }

                # Append each filtered dictionary to our incidents list
                incidents.append(incident_obj)

    # -------------------------------------------------------------------------
    # STEP 4: Handle Request Failures
    # -------------------------------------------------------------------------
    else:
        # Add an error dictionary if the WMATA request fails
        incidents.append({
            "error": f"Failed to retrieve incidents (HTTP {response.status_code})"
        })

    # -------------------------------------------------------------------------
    # STEP 5: Return JSON String
    # -------------------------------------------------------------------------
    # Convert the Python list of dictionaries into a JSON string using json.dumps()
    # indent=4 makes the output readable when viewed in a browser
    return json.dumps(incidents, indent=4)

# -----------------------------------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Run Flask’s built-in development server with debugging enabled
    app.run(debug=True)
