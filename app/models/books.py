from extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Adjust data type to float for price
    price_unit = db.Column(db.String(50), nullable=False, default='UGX')
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=False, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Add nullable=False
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)  # Add nullable=False
    user = db.relationship('User', backref='books')
    company = db.relationship('Company', backref='books')

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, title, pages, price, price_unit, publication_date, isbn, genre, description, image, company_id, user_id):
        self.title = title
        self.pages = pages
        self.price = price
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.image = image
        self.company_id = company_id
        self.user_id = user_id

    def get_full_name(self):
        return self.title

