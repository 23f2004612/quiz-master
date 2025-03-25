

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user
from flask_login import LoginManager
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from datetime import datetime
from auth import auth
from models import db, User, ActiveSession, Subject, Chapter, Quiz, Question
from forms import SubjectForm,ChapterForm,QuizForm,QuestionForm
from subject_CUD import sub_bp
from chapter_CUD import chap_bp
from quiz_CUD import quiz_bp
from question_CUD import ques_bp


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
        return redirect(url_for('login'))

    # User-specific content goes here
    return render_template('user_dashboard.html')


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()  # Ensure tables are created before adding users
        
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
        else:
            print("Admin user already exists.")

    app.run(debug=True)
