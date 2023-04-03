from app import app, db
from app.models import Appointment

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'appt': Appointment}