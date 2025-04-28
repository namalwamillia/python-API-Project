from extensions import db

class AddressBook(db.Model):
    __tablename__ = 'address_books'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users table
    full_name = db.Column(db.String(100), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), nullable=True)  # Optional field
    city_region = db.Column(db.String(100), nullable=False)  # Required field
    phone_number = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('address_books', lazy=True))

    def __init__(self, user_id, full_name, address_line1, city_region, phone_number, address_line2=None):
        self.user_id = user_id
        self.full_name = full_name
        self.address_line1 = address_line1
        self.city_region = city_region  # Make sure the constructor accepts 'city_region'
        self.phone_number = phone_number
        self.address_line2 = address_line2
