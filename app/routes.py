from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.models import Appointment
from app.forms import RegistrationForm
from datetime import datetime, timedelta
import humanize


@app.route('/')
def hello():
    return render_template('base.html')

@app.route('/appointments/book', methods=['GET', 'POST'])
def book():
    form = RegistrationForm()
    if form.validate_on_submit():
        appointment = Appointment()
    return render_template('book_apt.html', form=form)

@app.route('/appointments')
def select_appt():
    now = datetime.now()

    start_date = now
    end_date = now + timedelta(days=30)

    appointments = Appointment.query.filter(Appointment.start_time >= start_date,
                                            Appointment.end_time <= end_date).all()

    # Generate a list of dates
    dates = [start_date + timedelta(days=i) for i in range(0, 31)]

    # Generate a list of timeslots
    timeslots = [datetime.combine(d, datetime.min.time()) +
                 timedelta(hours=i) for d in dates for i in range(9, 17)]

    # Generate a list of busy timeslots
    busy_timeslots = []
    for appointment in appointments:
        busy_timeslots.extend(
            [t for t in timeslots if appointment.start_time <= t < appointment.end_time])

    # Generate a list of weeks and days
    """
    month = []
    week = []
    for date in dates:
        day = {
            'number': date.day,
            'timeslots': [t for t in timeslots if t.date() == date and t not in busy_timeslots]
        }
        week.append(day)
        if date.weekday() == 5:
            month.append(week)
            week = []
    if week:
        month.append(week)
    """

    return render_template('calendar.html', timeslots=timeslots, busy_timeslots=busy_timeslots)



@app.route('/contact')
def confirm_book():
    return 'Apointment confirmed'