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




# Need complaint id (PK) , user_id (FK) , location_url, siviarity, problem type as a multiple list and image_name list

class Complaints(db.Model):
    __tablename__ = "complaints"

    # Primary key for the complaint
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    # complaint title
    title = db.Column(db.Text, nullable=False)

    #complaint description
    description = db.Column(db.Text, nullable=False)

    # Location URL (could be a Google Maps URL or coordinates)
    location_url = db.Column(db.String(255))


    # Severity level (e.g., low, medium, high, critical)
    severity = db.Column(db.String(20), nullable=False)

    # Will store as: ["type1", "type2", "type3"]
    problem_types = db.Column(db.Text, nullable=False)

    # Will store as: ["image1.jpg", "image2.jpg"]
    image_names = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime)

    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)
