
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import ActiveSession, db, User 
from flask_login import current_user, login_required, login_user, logout_user

from controllers.forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
       
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for("auth.register"))
        
        else:
            # Create a new user and store it in the database
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                qualification=form.qualification.data,
                dob=form.dob.data,
                role="user"
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming you have a LoginForm class for username, password, and role fields
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data  # Ensure this matches your form field name
        role = form.role.data  # Role can be "admin" or "user"

        user = User.query.filter_by(username=username).first()  # Query user based on username
        
        if user and check_password_hash(user.password, password) and user.role == role:
            login_user(user)  
            # Redirect to the appropriate dashboard based on user role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            else:
                return redirect(url_for('user_dashboard'))  # Redirect to user dashboard
        else:
            flash('Login failed. Check your username, password, and role.', 'danger')
    
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    if current_user.role == 'admin':
        active_admin = ActiveSession.query.filter_by(user_id=current_user.id, role='admin').first()
        if active_admin:
            db.session.delete(active_admin)
            db.session.commit()

    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to home or login page