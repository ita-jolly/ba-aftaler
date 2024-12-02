import os
import requests
from flask import Flask, request, jsonify, make_response 
import db_service 
from flasgger import Swagger, swag_from 
from dotenv import load_dotenv 
from swagger.config import swagger_config 

load_dotenv() 

app = Flask(__name__) 
swagger = Swagger(app, config=swagger_config) 

# URL of the "biler" microservice
BILER_SERVICE_URL = os.getenv('BILER_SERVICE_URL')
KUNDER_SERVICE_URL = os.getenv('KUNDER_SERVICE_URL')


db_service.init() 

@app.route('/', methods=['GET']) 
def index(): 
    return "Welcome to API" 


@app.route('/aftaler', methods=['POST'])
def create_aftale():
    """Endpoint to create a new aftale."""
    try:
        # Parse the JSON request
        data = request.get_json()
        required_fields = ['aftale_id', 'cpr', 'nummerplade', 'aftale_type', 'start_dato', 'slut_dato']

        # Validate that all required fields are present
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if the nummerplade is available in the biler microservice
        nummerplade = data['nummerplade']
        response = requests.get(f"{BILER_SERVICE_URL}/biler")
        if response.status_code != 200:
            return jsonify({"error": "Could not communicate with the biler service"}), 500

        biler = response.json()
        # Find the relevant bil by nummerplade
        matching_bil = next((bil for bil in biler if bil['nummerplade'] == nummerplade), None)

        if not matching_bil:
            return jsonify({"error": f"Nummerplade {nummerplade} not found in biler database"}), 404
        
        # Check if udlejnings_status is True (car is not available for rental)
        if matching_bil['udlejnings_status']:
            return jsonify({"error": f"Nummerplade {nummerplade} is not available for rental"}), 400
        
        # Check if the cpr is available in the kunder microservice
        cpr = data['cpr']
        response = requests.get(f"{KUNDER_SERVICE_URL}/kunder")
        kunder = response.json()
        if kunder is None:
            return jsonify({"error": "Could not communicate with the kunder database"}), 500

        matching_kunde = next((kunde for kunde in kunder if kunde['cpr'] == cpr), None)
        if not matching_kunde:
            return jsonify({"error": f"Cpr {cpr} does not exists in kunder database"}), 400

        # Call the db_service to insert a new aftale
        result = db_service.create_aftale(
            aftale_id=data['aftale_id'],
            cpr=data['cpr'],
            nummerplade=data['nummerplade'],
            aftale_type=data['aftale_type'],
            start_dato=data['start_dato'],
            slut_dato=data['slut_dato']
        )

        # If insertion failed, return an error
        if not result:
            return jsonify({"error": "Could not create aftale. It may already exist."}), 409
        
         # After creating the aftale, update the udlejnings_status to True in the biler service
        update_response = requests.patch(
            f"{BILER_SERVICE_URL}/biler/{nummerplade}",
            json={"udlejnings_status": True}
        )
        
        if update_response.status_code != 200:
            return jsonify({"error": "Failed to update udlejnings_status in biler service"}), 500

        # Return the created aftale
        return jsonify({"message": "Aftale created successfully!", "aftale": result}), 201

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/aftaler', methods=['GET'])
def get_aftaler():
    aftaler = db_service.get_aftaler()

    if aftaler is None:
        response = make_response({'message': 'Ingen aftaler fundet'}, 404)
    else:
        response = make_response(aftaler, 200)

    return response

# @app.route('/gettemplate', methods=['GET']) 
# @swag_from('swagger/get_template.yml') 

if __name__ == '__main__': 
    app.run(debug=True, port=5001) 