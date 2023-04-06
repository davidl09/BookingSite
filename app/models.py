from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

    

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    phone_number = db.Column(db.String(24), index=True)
    start_time = db.Column(db.DateTime, index=True, unique=True)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(120))

    def __repr__(self):
        return '<Appointment ID: {}, First Name: {}, Start Time/Date: {}>'.format(self.id, self.first_name, datetime.strftime(self.start_time, "%Y-%m-%d_%H:%M"))
    
"""class AdminUser(db.Model):
    username = db.Column(db.string)"""
    

