import re
from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from app.models.users import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')

        if not all([name, phone_number, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        try:
            test_user = User(name='test', phone_number=phone_number, 
                        email='test@test.com', password='test')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        if User.query.filter_by(phone_number=phone_number).first():
            return jsonify({'error': 'Phone number already registered'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            name=name,
            phone_number=phone_number,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(days=365 * 100)
        )

        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'phone_number': new_user.phone_number,
                'role': new_user.role
            },
            'access_token': access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            return jsonify({'error': 'Phone number and password are required'}), 400

        cleaned_number = re.sub(r'[^\d]', '', phone_number)
        if len(cleaned_number) != 10:
            return jsonify({'error': 'Phone number must be exactly 10 digits'}), 400
        if not cleaned_number.isdigit():
            return jsonify({'error': 'Phone number must contain only numbers'}), 400

        user = User.query.filter_by(phone_number=cleaned_number).first()

        if not user:
            return jsonify({'error': 'Invalid phone number or password'}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid phone number or password'}), 401

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=365 * 100)
        )

        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'role': user.role
            },
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        current_user_id = get_jwt_identity()
        user_to_delete = User.query.get_or_404(id)
        current_user = User.query.get_or_404(int(current_user_id))

        if current_user_id != str(user_to_delete.id) and current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized: You can only delete your own account or you must be an admin'}), 403

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500