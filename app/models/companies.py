from extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='companies')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_type = db.Column(db.String(100), nullable=False)

    def __init__(self, name, origin, description, user_id, user_type, created_at=datetime.now()):
        super(Company, self).__init__()
        self.name = name
        self.origin = origin
        self.description = description
        self.user_id = user_id
        self.user_type = user_type
        self.created_at = created_at

    def get_full_name(self):
        return f"{self.name} {self.origin}"

    def to_dict(self):
        """
        Converts the Company object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "origin": self.origin,
            "description": self.description,
            "user_id": self.user_id,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
