from extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the User table
    message = db.Column(db.Text, nullable=False)  # Message content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the message is created

    user = db.relationship('User', backref=db.backref('messages', lazy=True))  # Relationship with User

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"<Message from User {self.user_id}: {self.message}>"
