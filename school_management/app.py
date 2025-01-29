from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.name}>'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Teacher {self.name}>'

# Create database if it doesn't exist (run this once)
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    with app.app_context():  # Add this if needed
        return render_template('about_us.html')
    
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')  

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()  # Date parsing
        grade = request.form['grade']
        address = request.form['address']

        new_student = Student(name=name, dob=dob, grade=grade, address=address)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:  # Handle potential errors
            db.session.rollback()  # Important: Rollback on error
            flash(f'Error adding student: {str(e)}', 'danger') # More informative error
            return render_template('students.html')  # Re-render the form

    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']

        new_teacher = Teacher(name=name, subject=subject)
        try:
            db.session.add(new_teacher)
            db.session.commit()
            flash('Teacher added successfully!', 'success')
            return redirect(url_for('teachers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding teacher: {str(e)}', 'danger')
            return render_template('teachers.html')

    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)


if __name__ == '__main__':
    app.run(debug=True)