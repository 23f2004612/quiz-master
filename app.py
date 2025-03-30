
from flask import Flask, render_template, redirect,url_for, flash, request
from flask_login import current_user, login_required
from flask_login import LoginManager
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from datetime import datetime
from controllers.auth import auth
from models.models import db, User, ActiveSession, Subject, Chapter, Quiz, Question,Score
from controllers.forms import SubjectForm
from controllers.subject_CUD import sub_bp
from controllers.chapter_CUD import chap_bp
from controllers.quiz_CUD import quiz_bp
from controllers.question_CUD import ques_bp
from controllers.quiz_handling import quiz_handle_auth
from flask import render_template
from controllers.user_search import user_search
from controllers.user_summary import user_sum
from controllers.admin_summary import admin_sum
from controllers.admin_search import admin_search
import plotly.graph_objs as go
from controllers.proj_routes import api
from flask import Flask, get_flashed_messages


# Initialize app and db
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\Kaushik KS\Documents\Quizmaster\database.db'  

db.init_app(app) 

@app.before_request
def clear_flash_messages():
    get_flashed_messages()

# Registering the blueprint for authentication-related routes with the URL prefix "/auth"
app.register_blueprint(auth, url_prefix="/auth")

# Registering the blueprint for subject-related routes with the URL prefix "/sub_auth"
app.register_blueprint(sub_bp, url_prefix="/sub_auth")

# Registering the blueprint for chapter-related routes with the URL prefix "/chap_auth"
app.register_blueprint(chap_bp, url_prefix="/chap_auth")

# Registering the blueprint for quiz-related routes with the URL prefix "/quiz_auth"
app.register_blueprint(quiz_bp, url_prefix="/quiz_auth")

# Registering the blueprint for question-related routes with the URL prefix "/ques_auth"
app.register_blueprint(ques_bp, url_prefix="/ques_auth")

# Registering the blueprint for handling quiz authentication with the URL prefix "/quiz_handle_auth"
app.register_blueprint(quiz_handle_auth, url_prefix="/quiz_handle_auth")

# Registering the blueprint for user search functionality with the URL prefix "/user_search"
app.register_blueprint(user_search, url_prefix="/user_search")

# Registering the blueprint for user summary routes with the URL prefix "/user_sum"
app.register_blueprint(user_sum, url_prefix="/user_sum")

# Registering the blueprint for admin summary routes with the URL prefix "/admin_sum"
app.register_blueprint(admin_sum, url_prefix="/admin_sum")

# Registering the blueprint for admin search functionality with the URL prefix "/admin_search"
app.register_blueprint(admin_search, url_prefix="/admin_search")

# Registering the blueprint for API routes with the URL prefix "/api"
app.register_blueprint(api, url_prefix="/api")


# Setting up database migration support using Flask-Migrate
migrate = Migrate(app, db)

# Initializing the LoginManager for handling user authentication
login_manager = LoginManager(app)

# Associating the app with the LoginManager
login_manager.init_app(app)

# Setting the login view route for unauthorized users
login_manager.login_view = 'login'

# Load the user from the database based on username
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)  

# Route for rendering the home page for unauthenticated users
@app.route('/')
def home():
    return render_template('home.html')  # Render the home page template

# Admin dashboard route, accessible only to logged-in admin users
@app.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # Redirect non-admin users to the user dashboard
    if current_user.role != 'admin':
        flash('You do not have admin rights.', 'danger')
        return redirect(url_for('user_dashboard'))

    # Check if an active admin session already exists
    active_admin = ActiveSession.query.filter_by(role='admin').first()
    if active_admin and active_admin.user_id != current_user.id:
        flash('Another admin is already active.', 'danger')
        return redirect(url_for('auth.login'))

    # Create a new active admin session if one does not exist
    if not active_admin:
        new_session = ActiveSession(user_id=current_user.id, role='admin')
        db.session.add(new_session)
        db.session.commit()

    # Fetch all subjects and create a SubjectForm instance
    subs = Subject.query.all()  # Fetch subjects
    form = SubjectForm()  # Create an instance of the form

    # Render the admin dashboard template with the form and subjects
    return render_template('admin_dashboard.html', form=form, subjects=subs)


# User dashboard route, accessible only to logged-in user accounts
@app.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    # Redirect non-user roles to the login page
    if current_user.role != 'user':
        flash('You must be a user to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Retrieve quiz attempts for the current user
    quiz_attempts = Score.query.filter_by(user_id=current_user.id).all()
    attempted_quiz_ids = {attempt.quiz_id for attempt in quiz_attempts}

    # Fetch all upcoming quizzes
    upcoming_quizzes = Quiz.query.all()

    quizzes_with_questions = []

    # Loop through quizzes and gather quiz details
    for quiz in upcoming_quizzes:
        question_count = Question.query.filter_by(quiz_id=quiz.id).count()
        chapter = quiz.chapter
        subject = chapter.subject if chapter else None
        is_attempted = quiz.id in attempted_quiz_ids
        score = None

        # Retrieve the user's score if the quiz is attempted
        if is_attempted:
            attempt = next((attempt for attempt in quiz_attempts if attempt.quiz_id == quiz.id), None)
            if attempt:
                score = attempt.score
            
        # Get subject and chapter names
        subject_name = subject.name if subject else "Unknown"
        chapter_name = chapter.name if chapter else "Unknown"
        quiz_date = quiz.date.strftime('%Y-%m-%d') if quiz.date else "Unknown Date" 

        # Append quiz details to the list
        quizzes_with_questions.append({
            "id": quiz.id,
            "subject_name": subject_name,
            "chapter_name": chapter_name,
            "date": quiz_date,
            "attempted": is_attempted,
            "score": score
        })
    
    # Render the user dashboard template with quizzes
    return render_template('user_dashboard.html', quizzes=quizzes_with_questions)

if __name__ == "__main__":
    with app.app_context():
          # Ensure tables are created before adding users
        
        admin = User.query.filter_by(name='Admin').first()
        dob_input = 'NA'
        if not admin:  # Avoid duplicate entries
            admin = User(
                username='admin@iitm.ac.in',
                password=generate_password_hash('adminkaushik'),  # Use hashed password
                name='Admin',
                qualification='N/A',
                dob=None if dob_input == 'NA' else datetime.strptime(dob_input, '%Y-%m-%d').date(),
                role='admin'  # Ensure lowercase 'admin' as per your form choices
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")

    app.run(debug=True)
