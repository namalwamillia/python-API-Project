from flask import Blueprint, request, jsonify
from app.models.users import User
from extensions import db, bcrypt
from app.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
)
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token
import logging
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity




auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# User registration
@auth.route('/register', methods=['POST'])
def register_users():
    try:
        data = request.get_json()

        # Validate user data (e.g., check for required fields, email format, password strength)
        # ... (add necessary validation checks)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')
        biography = data.get('biography')
        user_type = data.get('user_type', 'authors')
        image = data.get('image')

        # Check for existing user with the same email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=contact,
            password=hashed_password,
            biography=biography,
            user_type=user_type,
            image=image
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#logging in users

# @auth.route('/login', methods=['POST'])
# def login():
#     try:
#         email = request.json.get('email')
#         password = request.json.get('password')

#         if not email or not password:
#             return jsonify({'error': 'Missing email or password'}), 400

#         user = User.query.filter_by(email=email).first()
#         if not user:
#             return jsonify({'error': 'User not found'}), 401

#         if not bcrypt.check_password_hash(user.password, password):
#             return jsonify({'error': 'Invalid password'}), 401

#         access_token = create_access_token(identity=user.id)
#         return jsonify({
#             'user': {
#                 'id': user.id,
#                 'username': user.get_full_name(),
#                 'email': user.email,
#                 'access_token': access_token,
#                 'type': user.user_type
#             },
#             'message': 'You have successfully logged into your account'
#         }), 200
#     except Exception as e:
#         # Log the exception for debugging
#         logging.error(f"An error occurred during login: {str(e)}")
#         return jsonify({'error': 'Internal server error'}), 500


# Logging in users
@auth.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid password'}), 401

        # Generate access token and refresh token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'user': {
                'id': user.id,
                'username': user.get_full_name(),
                'email': user.email,
                'access_token': access_token,
                'refresh_token': refresh_token,  # Add refresh token to response
                'type': user.user_type
            },
            'message': 'You have successfully logged into your account'
        }), 200
    except Exception as e:
        logging.error(f"An error occurred during login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    #Get refresh_token

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Require a refresh token for this route
def refresh():
    current_user = get_jwt_identity()  # Get the user id from the refresh token
    new_access_token = create_access_token(identity=current_user)  # Create a new access token

    return jsonify({
        'access_token': new_access_token
    }), 200




    #Get all users
@auth.route('/users/', methods=('POST',))  # Use methods as a tuple
def get_all_users():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact': user.contact,
            'user_type': user.user_type,
            'biography': user.biography,
            'image':user.image,
            'created_at':user.created_at,
            'password':user.password
        }
        output.append(user_data)
    return jsonify({'users': output})

# Get a specific user
@auth.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact': user.contact,
            'user_type': user.user_type,
            'biography': user.biography,
            'image':user.image,
            'created_at':user.created_at,
            'password':user.password
            
    }
    return jsonify(user_data)


# Update a user
@auth.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.contact = data.get('contact', user.contact)
        user.user_type = data.get('user_type', user.user_type)
        password = data.get('password')
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.biography = data.get('biography', user.biography)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    # Delete a user
@auth.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500
    




    

