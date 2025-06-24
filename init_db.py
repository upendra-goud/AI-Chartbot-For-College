from flask_sqlalchemy import SQLAlchemy
from models import db, User, Student
from auth import hash_password
from app import app

try:
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='student1').first():
            user = User(username='student1', password=hash_password('student123'), role='student')
            db.session.add(user)
            db.session.commit()
            student = Student(user_id=user.id, roll_no='2024CSE001', balance_due=85000.00, attendance='87%')
            db.session.add(student)
            db.session.commit()
        if not User.query.filter_by(username='teacher1').first():
            teacher = User(username='teacher1', password=hash_password('teacher123'), role='teacher')
            db.session.add(teacher)
            db.session.commit()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password=hash_password('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
        print("Database initialized with sample data.")
except Exception as e:
    print(f"Error initializing database: {e}")