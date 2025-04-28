import re
from sqlalchemy.orm import validates
from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    successful_orders = db.Column(db.Integer, default=0)
    cancelled_orders = db.Column(db.Integer, default=0)

    def __init__(self, name, phone_number, email, password, role='customer'):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.role = role

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        # Remove any non-digit characters
        cleaned_number = re.sub(r'[^\d]', '', phone_number)
        
        # Validate length (must be exactly 10 digits)
        if len(cleaned_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        
        # Check if it's all digits
        if not cleaned_number.isdigit():
            raise ValueError("Phone number must contain only numbers")
        
        return cleaned_number