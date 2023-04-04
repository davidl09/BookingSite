from app import app, db
from app.models import Appointment
from datetime import datetime, timedelta

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'appt': Appointment}