from wmata_api import app   # Import the Flask app instance from your main module
import json
import unittest

class WMATATest(unittest.TestCase):
    # -------------------------------------------------------------------------
    # 1. Ensure both endpoints return a 200 HTTP status code
    # -------------------------------------------------------------------------
    def test_http_success(self):
        # Simulate HTTP GET request to /incidents/escalators
        escalator_response = app.test_client().get('/incidents/escalators')
        # Assert that the escalator endpoint returns HTTP 200
        self.assertEqual(escalator_response.status_code, 200, 
                         "Expected 200 status for /incidents/escalators")

        # Simulate HTTP GET request to /incidents/elevators
        elevator_response = app.test_client().get('/incidents/elevators')
        # Assert that the elevator endpoint returns HTTP 200
        self.assertEqual(elevator_response.status_code, 200, 
                         "Expected 200 status for /incidents/elevators")

    # -------------------------------------------------------------------------
    # 2. Ensure all returned incidents have the 4 required fields
    # -------------------------------------------------------------------------
    def test_required_fields(self):
        # Define the fields that must exist in every incident record
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        # Send a request to the escalators endpoint
        response = app.test_client().get('/incidents/escalators')
        # Decode the JSON response from bytes → string → Python list
        json_response = json.loads(response.data.decode())

        # Iterate through each incident and check each field
        for incident in json_response:
            for field in required_fields:
                # Assert that each required field key exists in the dictionary
                self.assertIn(field, incident, 
                              f"Missing field '{field}' in response object: {incident}")

    # -------------------------------------------------------------------------
    # 3. Ensure all entries returned by /incidents/escalators have UnitType = "ESCALATOR"
    # -------------------------------------------------------------------------
    def test_escalators(self):
        # Request escalator data
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        # Loop through each incident and verify its UnitType value
        for incident in json_response:
            if "UnitType" in incident:  # Avoid crashing on error messages
                self.assertEqual(incident["UnitType"].upper(), "ESCALATOR",
                                 f"Unexpected UnitType: {incident['UnitType']}")

    # -------------------------------------------------------------------------
    # 4. Ensure all entries returned by /incidents/elevators have UnitType = "ELEVATOR"
    # -------------------------------------------------------------------------
    def test_elevators(self):
        # Request elevator data
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())

        # Loop through each incident and verify its UnitType value
        for incident in json_response:
            if "UnitType" in incident:  # Avoid crashing on error messages
                self.assertEqual(incident["UnitType"].upper(), "ELEVATOR",
                                 f"Unexpected UnitType: {incident['UnitType']}")

# -------------------------------------------------------------------------
# Run tests when executed directly
# -------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
