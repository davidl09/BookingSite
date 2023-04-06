from flask import render_template, redirect, flash, url_for, request
from sqlalchemy import and_, or_
from app import app, db
from app.models import Appointment
from app.forms import RegistrationForm
from datetime import datetime, timedelta, time
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

@app.route('/appointments/day')
def select_appt_time():
    app_day = datetime.strptime(request.args.get('datetime'), "%Y-%m-%d %H:%M:%S")
    appt_times = [datetime(year=app_day.year, month=app_day.month, day=app_day.day, hour=i, minute=j) for i in range(9, 17) for j in range(0, 60, 15)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    return render_template('calendar_day.html', daytimes=appt_times, months=months)

@app.route('/appointments', methods=['GET', 'POST'])
def appt_select_day():

    now = datetime.now()

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays = [weekday[:1] for weekday in weekdays]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    start_time=datetime(now.year, month=now.month, day=now.day + 1, hour=9, minute=0)
    cal_start_date = start_time - timedelta(days=start_time.weekday())

    date_nums = [cal_start_date + timedelta(days=i) for i in range(35)]

    return render_template('calendar_month.html', start_time=start_time, weekdays=weekdays, date_nums=date_nums, months=months)


"""
    now = datetime.now()
    start_date = datetime(now.year, now.month, now.day, 9, 0, 0)
    end_date = start_date + timedelta(days=30)

    appointments = db.session.query(Appointment).all()

    timeslots = []
    for i in range(1, timedelta(start_date.day, end_date.day).days): #fix this, not filtering appointments properly
        for j in range(8):
            if db.session.query(Appointment).filter(and_(
                datetime(Appointment.start_time).hour == datetime(start_date + timedelta(days=i, hours=j)).hour,
                datetime(Appointment.start_time).day == datetime(start_date + timedelta(days=i, hours=j)).day
                )).first() == None:
                timeslots.append(start_date + timedelta(days=i, hours=j))
     """