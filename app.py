

from random import shuffle
from flask import Flask, render_template, redirect, session, url_for, flash, request
from flask_login import current_user, login_required, logout_user
from flask_login import LoginManager
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from datetime import datetime
from auth import auth
from models import db, User, ActiveSession, Subject, Chapter, Quiz, Question,Score
from forms import SubjectForm,ChapterForm,QuizForm,QuestionForm
from subject_CUD import sub_bp
from chapter_CUD import chap_bp
from quiz_CUD import quiz_bp
from question_CUD import ques_bp
from quiz_handling import quiz_handle_auth


# Initialize app and db
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\Kaushik KS\Documents\Quizmaster\database.db'  

db.init_app(app) 
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(sub_bp, url_prefix="/sub_auth") 
app.register_blueprint(chap_bp, url_prefix="/chap_auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz_auth")
app.register_blueprint(ques_bp, url_prefix="/ques_auth")
app.register_blueprint(quiz_handle_auth, url_prefix="/quiz_handle_auth")

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)  

@app.route('/')
def home():
    return render_template('home.html')  # Render the home page for unauthenticated users

@app.route('/admin/dashboard',methods = ['GET','POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You do not have admin rights.', 'danger')
        return redirect(url_for('user_dashboard'))

    active_admin = ActiveSession.query.filter_by(role='admin').first()
    if active_admin and active_admin.user_id != current_user.id:
        flash('Another admin is already active.', 'danger')
        return redirect(url_for('auth.login'))

    # Create a new active session if not exists
    if not active_admin:
        new_session = ActiveSession(user_id=current_user.id, role='admin')
        db.session.add(new_session)
        db.session.commit()

    subs = Subject.query.all()  # Fetch subjects
    form = SubjectForm()  # Create an instance of the form

    return render_template('admin_dashboard.html', form=form, subjects=subs)


@app.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if current_user.role != 'user':
        flash('You must be a user to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    
    quiz_attempts = Score.query.filter_by(user_id=current_user.id).all()
    attempted_quiz_ids = {attempt.quiz_id for attempt in quiz_attempts}

    upcoming_quizzes = Quiz.query.all()

    quizzes_with_questions = []
    for quiz in upcoming_quizzes:
        question_count = Question.query.filter_by(quiz_id=quiz.id).count()
        is_attempted = quiz.id in attempted_quiz_ids
        score = None

        if is_attempted:
            attempt = next((attempt for attempt in quiz_attempts if attempt.quiz_id == quiz.id), None)
            if attempt:
                score = attempt.score
            
            
        quizzes_with_questions.append({
            "id": quiz.id,
            "chapter_id": quiz.chapter_id,
            "date": quiz.date.strftime('%Y-%m-%d'),
            "duration": quiz.duration,
            "num_questions": question_count,
            "attempted": is_attempted,
            "score": score
        })
    return render_template('user_dashboard.html',quizzes = quizzes_with_questions)


if __name__ == "__main__":
    with app.app_context():
          # Ensure tables are created before adding users
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:  # Avoid duplicate entries
            admin = User(
                username='admin',
                password=generate_password_hash('adminkaushik'),  # Use hashed password
                name='Admin',
                qualification='N/A',
                dob=datetime.strptime('2005-04-08', '%Y-%m-%d').date(),
                role='admin'  # Ensure lowercase 'admin' as per your form choices
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
    
            user1 = User(
                username='kaushik',
                password=generate_password_hash('kaushik123'),  # Use hashed password
                name='Kaushik',
                qualification='N/A',
                dob=datetime.strptime('2005-04-08', '%Y-%m-%d').date(),
                role='user'  # Ensure lowercase 'admin' as per your form choices
                )
        
            db.session.add(user1)
            db.session.commit()
    app.run(debug=True)
