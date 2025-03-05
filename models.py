from app import db
from datetime import datetime



class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50),nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime)
    points = db.Column(db.Integer)
