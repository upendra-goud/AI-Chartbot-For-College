from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
from models import db, User, Student, Chat
from auth import verify_user, hash_password
from chatbot import get_response

app = Flask(__name__)
app.secret_key = 'ace-college-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://college_user:78657865@localhost/college'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt: username={username}, password={'*' * len(password)} (length={len(password)})")
        user = verify_user(username, password)
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            logging.info(f"User {username} logged in with role {user.role}")
            flash('Login successful!', 'success')
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        logging.error(f"Failed login attempt for username: {username}")
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    session.clear()
    logging.info(f"User {username} logged out")
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        flash('Student record not found', 'danger')
        return redirect(url_for('home'))
    chats = Chat.query.filter_by(user_id=session['user_id']).order_by(Chat.timestamp.desc()).limit(5).all()
    return render_template('student/dashboard.html', student=student, chats=chats)

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))
    students = Student.query.all()
    chats = Chat.query.filter_by(user_id=session['user_id']).order_by(Chat.timestamp.desc()).limit(5).all()
    return render_template('teacher/dashboard.html', students=students, chats=chats)

@app.route('/teacher/update/<int:id>', methods=['GET', 'POST'])
def teacher_update(id):
    if session.get('role') != 'teacher':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.balance = float(request.form.get('balance'))
        student.attendance = request.form.get('attendance')
        db.session.commit()
        logging.info(f"Teacher updated student ID {id}: balance={student.balance}, attendance={student.attendance}")
        flash('Student data updated!', 'success')
        return redirect(url_for('teacher_dashboard'))
    return render_template('teacher/update.html', student=student)

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))
    students = Student.query.all()
    chats = Chat.query.order_by(Chat.timestamp.desc()).limit(10).all()
    return render_template('admin/dashboard.html', students=students, chats=chats)

@app.route('/admin/manage', methods=['GET', 'POST'])
def admin_manage():
    if session.get('role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if not all([username, password, role]):
            flash('All fields are required', 'danger')
            return redirect(url_for('admin_manage'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('admin_manage'))
        user = User(username=username, password=hash_password(password), role=role)
        db.session.add(user)
        db.session.flush()
        if role == 'student':
            roll_no = request.form.get('roll_no')
            if not roll_no:
                flash('Roll number is required for students', 'danger')
                db.session.rollback()
                return redirect(url_for('admin_manage'))
            existing_student = Student.query.filter_by(roll_no=roll_no).first()
            if existing_student:
                flash('Roll number already exists', 'danger')
                db.session.rollback()
                return redirect(url_for('admin_manage'))
            student = Student(user_id=user.id, roll_no=roll_no, balance=100000, attendance='0.00')
            db.session.add(student)
        db.session.commit()
        logging.info(f"Admin created user: {username} with role {role}")
        flash(f'{role.capitalize()} added successfully!', 'success')
        return redirect(url_for('admin_manage'))
    users = User.query.all()
    return render_template('admin/manage.html', users=users)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    user_id = session.get('user_id')
    role = session.get('role')
    response = get_response(user_input, role, user_id)
    if user_id:
        chat = Chat(user_id=user_id, message=user_input, response=response, timestamp=datetime.utcnow())
        db.session.add(chat)
        db.session.commit()
        logging.info(f"Chat saved for user_id {user_id}: {user_input}")
    return jsonify({'response': response})

@app.route('/api/chat-history', methods=['GET'])
def chat_history():
    if not session.get('user_id'):
        return jsonify([]), 401
    chats = Chat.query.filter_by(user_id=session.get('user_id')).order_by(Chat.timestamp.desc()).limit(10).all()
    return jsonify([{'message': c.message, 'response': c.response, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in chats])

@app.route('/pay_fees', methods=['POST'])
def pay_fees():
    if session.get('role') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    amount = float(request.form.get('amount'))
    if amount <= 0 or amount > student.balance:
        return jsonify({'error': 'Invalid amount'}), 400
    student.balance -= amount
    db.session.commit()
    logging.info(f"Payment of {amount} processed for student ID {student.id}")
    return jsonify({'message': f'Paid ₹{amount:.2f}. New balance: ₹{student.balance:.2f}'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)