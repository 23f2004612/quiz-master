
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Subject, ActiveSession
from forms import SubjectForm

# Create a Blueprint
sub_bp = Blueprint("sub_auth", __name__)

@sub_bp.route('/admin/add_subject', methods=['POST'])
@login_required
def add_subject():
    # Check if the current user is an admin
    if current_user.role != 'admin':
        flash('You do not have admin rights.', 'danger')
        return redirect(url_for('user_dashboard'))

    # Check for an active admin session
    active_admin = ActiveSession.query.filter_by(role='admin').first()
    if active_admin and active_admin.user_id != current_user.id:
        flash('Another admin is already active.', 'danger')
        return redirect(url_for('auth.login'))

    form = SubjectForm()  # Create form instance

    if form.validate_on_submit():  # Validate and submit
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('New subject added!', 'success')
        return redirect(url_for('admin_dashboard'))

    flash('Form submission failed!', 'danger')
    return redirect(url_for('admin_dashboard'))


@sub_bp.route('/admin/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    subject = Subject.query.get(id)
    if not subject:
        flash('Subject not found!', 'error')
        return redirect(url_for('admin_dashboard'))

    form = SubjectForm(obj=subject)  # Populate the form with the current subject data
    
    if request.method == 'POST':  # Handle form submission
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    else:
        flash(f'Form validation failed: {form.errors}', 'error')  

    return render_template('edit_subject.html',form = form,subject = subject)

@sub_bp.route('/admin/delete_subject/<int:subject_id>', methods=['POST'])
@login_required

def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)  # Remove the subject from the database
        db.session.commit()  # Commit the changes
        flash('Subject deleted successfully!', 'success')
    else:
        flash('Subject not found!', 'error')
    return redirect(url_for('admin_dashboard'))