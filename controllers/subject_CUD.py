
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, Subject, ActiveSession
from controllers.forms import SubjectForm

# Create a Blueprint
sub_bp = Blueprint("sub_auth", __name__)

# Route to add a new subject (only admins can access this route)
@sub_bp.route('/admin/add_subject', methods=['POST'])
@login_required
def add_subject():
    # Making sure only admins can add subjects
    if current_user.role != 'admin':
        flash('You do not have admin rights.', 'danger')
        return redirect(url_for('user_dashboard'))

    # Checking if there's already an active admin session
    active_admin = ActiveSession.query.filter_by(role='admin').first()
    if active_admin and active_admin.user_id != current_user.id:
        flash('Another admin is already active.', 'danger')
        return redirect(url_for('auth.login'))

    form = SubjectForm()  # Creating the form instance

    # If the form submission is legit
    if form.validate_on_submit():
        # Add the new subject to the database
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('New subject added!', 'success')  # Success flash message
        return redirect(url_for('admin_dashboard'))

    # If the form submission fails
    flash('Form submission failed!', 'danger')
    return redirect(url_for('admin_dashboard'))


# Route to edit an existing subject by ID
@sub_bp.route('/admin/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    subject = Subject.query.get(id)
    
    # If the subject doesn't exist
    if not subject:
        flash('Subject not found!', 'error')
        return redirect(url_for('admin_dashboard'))

    form = SubjectForm(obj=subject)  # Prefill the form with existing data

    # When the form is submitted
    if request.method == 'POST':
        # Update the subject details
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        flash('Subject updated successfully!', 'success')  # Success flash message
        return redirect(url_for('admin_dashboard'))
    else:
        # If form validation fails
        flash(f'Form validation failed: {form.errors}', 'error')

    # Render the edit page with the form
    return render_template('edit_subject.html', form=form, subject=subject)


# Route to delete a subject by ID
@sub_bp.route('/admin/delete_subject/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    
    # If the subject exists
    if subject:
        # Remove it from the database
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!', 'success')  # Success flash message
    else:
        # If the subject isn't found
        flash('Subject not found!', 'error')
        
    return redirect(url_for('admin_dashboard'))
