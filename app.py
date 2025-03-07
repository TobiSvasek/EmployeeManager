from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlsplit
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_present = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_authenticated = db.Column(db.Boolean, default=False)  # Add this line

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    clock_in_time = db.Column(db.DateTime, nullable=True)
    clock_out_time = db.Column(db.DateTime, nullable=True)
    total_time = db.Column(db.Float, nullable=True)


@app.route('/')
def index():
    return redirect(url_for('login'))

from urllib.parse import urlsplit

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['employee_name']
        password = request.form['password']
        employee = Employee.query.filter_by(name=name).first()

        if employee and employee.check_password(password):
            session['employee_id'] = employee.id
            session['login_time'] = datetime.now().timestamp()  # Set login timestamp
            employee.is_authenticated = True
            db.session.commit()
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('clock')
            if employee.is_admin:
                return redirect(next_page)
            else:
                return redirect(next_page)
        else:
            error = "Invalid credentials. Please try again."

    return render_template('login.html', error=error)

@app.route('/clock', methods=['GET', 'POST'])
def clock():
    if 'employee_id' not in session:
        return redirect(url_for('login'))

    employee = Employee.query.get(session['employee_id'])
    if not employee.is_authenticated:
        return redirect(url_for('login'))

    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.form['action']
        if action == 'clock_in':
            active_attendance = Attendance.query.filter_by(employee_id=employee.id, clock_out_time=None).first()
            if active_attendance:
                error_message = "You are already clocked in."
            else:
                attendance = Attendance(employee_id=employee.id, clock_in_time=datetime.now())
                employee.is_present = True
                db.session.add(attendance)
                db.session.commit()
                success_message = "Clocked in successfully!"
        elif action == 'clock_out':
            attendance = Attendance.query.filter_by(employee_id=employee.id, clock_out_time=None).first()
            if attendance:
                attendance.clock_out_time = datetime.now()
                attendance.total_time = (attendance.clock_out_time - attendance.clock_in_time).total_seconds() / 3600.0
                employee.is_present = False
                db.session.commit()
                success_message = "Clocked out successfully!"

    employees = Employee.query.all() if employee.is_admin else None
    attendances = Attendance.query.all() if employee.is_admin else None

    return render_template('clock.html', employee=employee, success_message=success_message, error_message=error_message, employees=employees, attendances=attendances)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        is_admin = 'is_admin' in request.form

        new_employee = Employee(name=name, is_admin=is_admin)
        new_employee.set_password(password)

        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for('clock'))

    return render_template('add_employee.html')

@app.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    return redirect(request.referrer)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)