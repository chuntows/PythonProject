from datetime import datetime

from flask_login import UserMixin

from src import bcrypt, db
from config import Config


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='sinhvien')  # Các giá trị: 'sinhvien', 'giangvien', 'admin'

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.role = role



    def __repr__(self):
        return f"<user {self.username} ({self.email})>"
