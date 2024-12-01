import os
from flask import Flask, request, jsonify, make_response 
import db_service 
from flasgger import Swagger, swag_from 
from dotenv import load_dotenv 
from swagger.config import swagger_config 

load_dotenv() 

app = Flask(__name__) 
swagger = Swagger(app, config=swagger_config) 

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

        # Return the created aftale
        return jsonify({"message": "Aftale created successfully!", "aftale": result}), 201

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



# @app.route('/gettemplate', methods=['GET']) 
# @swag_from('swagger/get_template.yml') 

if __name__ == '__main__': 
    app.run(debug=True) 