# app/utils/decorators.py
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from app.models.users import User

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__  # Preserve the original function name to avoid conflicts
    return wrapper