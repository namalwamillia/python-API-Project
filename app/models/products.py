from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='available')  # e.g., 'available', 'out_of_stock'
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    details = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    total_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, category, name, price, status='available', description=None, details=None, image=None, rating=0.0, total_balance=0.0):
        self.category = category
        self.name = name
        self.status = status
        self.price = price
        self.description = description
        self.details = details
        self.image = image
        self.rating = rating
        self.total_balance = total_balance