from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.models import Appointment
from app.forms import RegistrationForm
from datetime import datetime, timedelta
import humanize


@app.route('/')
@app.route('/home')
def hello():
    return render_template('base.html')

@app.route('/appointments/book', methods=['GET', 'POST'])
def book():
    form = RegistrationForm()
    if form.validate_on_submit():
        appointment = Appointment()
        appointment.first_name = str(form.first_name)
        appointment.last_name = str(form.last_name)
        appointment.email = str(form.email)
        appointment.phone_number = str(form.phone_number)
        start_time=request.args.get('start_datetime')
        appointment.start_time = datetime.strptime(start_time, '%Y-%m-%d_%H:%M')
        appointment.end_time = (datetime.strptime(start_time, '%Y-%m-%d_%H:%M') + timedelta(hours=1))
        appointment.location = 'insert location'
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('confirmation', 
                                start_datetime=start_time, 
                                location=appointment.location, 
                                email=form.email))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")
    return render_template('book_apt.html', form=form)

@app.route('/appointments/confirmation')
def confirmation():
    return render_template('confirmation.html', timeslot=datetime.strptime(request.args.get('start_datetime'), '%Y-%m-%d_%H:%M'), 
                           location=request.args.get('location'), email=request.args.get('email'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/appointments')
def select_appt():
    now = datetime.now()

    start_date = now + timedelta(days=1)
    end_date = now + timedelta(days=30)

    appointments = Appointment.query.filter(Appointment.start_time >= start_date,
                                            Appointment.end_time <= end_date).all()

    dates = [start_date + timedelta(days=i) for i in range(0, 31)]

    timeslots = [datetime.combine(d, datetime.min.time()) +
                 timedelta(hours=i) for d in dates for i in range(9, 17)]

    busy_timeslots = []
    for appointment in appointments:
        busy_timeslots.extend(
            [t for t in timeslots if appointment.start_time <= t < appointment.end_time])


    return render_template('calendar.html', timeslots=timeslots, busy_timeslots=busy_timeslots)



@app.route('/contact')
def confirm_book(timeslot):
    return render_template('', timeslot=timeslot)