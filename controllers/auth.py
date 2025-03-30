
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import ActiveSession, db, User 
from flask_login import current_user, login_required, login_user, logout_user

from controllers.forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Initialize the registration form to gather user details

    if form.validate_on_submit():  # Check if all form fields pass validation (e.g., required fields, correct format)

        user = User.query.filter_by(username=form.username.data).first()  # Check if the username already exists in the database

        if user:  # If a matching username is found, inform the user
            flash('Username already exists. Please choose a different one.', 'danger')  # Display error message
            return redirect(url_for("auth.register"))  # Reload the registration page so the user can try again
        else:
            # Create a new user with hashed password to enhance security
            hashed_password = generate_password_hash(form.password.data)  # Hash the password before storing it in the database
            new_user = User(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                qualification=form.qualification.data,
                dob=form.dob.data,
                role="user"  # Setting default role as 'user' during registration
            )
            db.session.add(new_user)  # Add the new user object to the session
            db.session.commit()  # Commit changes to store the user in the database
            flash('Account created successfully! You can now log in.', 'success')  # Inform the user of successful registration
            return redirect(url_for('auth.login'))  # Redirect to the login page to let the user log in

    return render_template('register.html', form=form)  # Display the registration form if validation fails or if request is GET


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Initialize the login form to capture credentials
    if form.validate_on_submit():  # Validate the form fields (e.g., required inputs, role selection)
        username = form.username.data  # Retrieve entered username
        password = form.password.data  # Retrieve entered password
        role = form.role.data  # Get selected role (admin or user)

        user = User.query.filter_by(username=username).first()  # Fetch user data from the database based on username

        # Check if user exists, password matches, and role matches
        if user and check_password_hash(user.password, password) and user.role == role:
            login_user(user)  # Authenticate and log the user in
            # Redirect to appropriate dashboard based on the user's role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))  # Redirect admin to admin dashboard
            else:
                return redirect(url_for('user_dashboard'))  # Redirect regular user to user dashboard
        else:
            flash('Login failed. Check your username, password, and role.', 'danger')  # Inform user of incorrect credentials or role

    return render_template('login.html', form=form)  # Show login form again if validation fails or request is GET


@auth.route('/logout')
def logout():
    if current_user.role == 'admin':  # Check if the logged-in user is an admin
        active_admin = ActiveSession.query.filter_by(user_id=current_user.id, role='admin').first()  # Get active session
        if active_admin:  # If an active admin session is found
            db.session.delete(active_admin)  # Remove the admin's active session from the database
            db.session.commit()  # Commit the session removal

    logout_user()  # Log out the current user and end the session
    flash('You have been logged out successfully.', 'info')  # Confirmation message
    return redirect(url_for('auth.login'))  # Redirect back to the login page after logout

