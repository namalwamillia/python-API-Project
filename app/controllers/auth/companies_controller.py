from flask import Blueprint, request, jsonify
from app.models.companies import Company  # Import Company from models
from app import db
from datetime import datetime

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register_company():
    try:
        # Extract data from request
        data = request.json

        # Basic input validation
        if not all([data.get(field) for field in ['name', 'origin', 'description', 'user_id', 'user_type']]):
            return jsonify({"error": "All fields are required"}), 400

        # Create a new company
        new_company = Company(
            name=data['name'],
            origin=data['origin'],
            description=data['description'],
            user_id=data['user_id'],
            user_type=data['user_type'],
           created_at=data.get('created_at', datetime.now())  # Handle optional created_at
        )

        # Add and commit to database
        db.session.add(new_company)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Company '{new_company.name}' has been registered"}), 201

    except Exception as e:
        # Handle exceptions appropriately (e.g., database errors, validation errors)
        return jsonify({"error": str(e)}), 500





