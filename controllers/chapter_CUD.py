
from flask import Blueprint, flash, redirect, render_template, request, url_for
from controllers.forms import ChapterForm
from models.models import Chapter, Subject,db

chap_bp = Blueprint("chap_auth", __name__)

# Route to add a new chapter
@chap_bp.route('/admin/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    subjects = Subject.query.all()  # Grab all the subjects from the database

    # If there are no subjects, redirect back with a warning
    if not subjects:  
        flash("No subjects available. Please create a subject first.", "danger")
        return redirect(url_for('admin_dashboard'))

    # When the form is submitted
    if request.method == 'POST':  
        name = request.form['name']
        description = request.form['description']
        subject_id = request.form['subject_id']

        # Making a new chapter object with the provided data
        chapter = Chapter(
            name=name,
            description=description,
            subject_id=subject_id
        )

        try:
            # Save the new chapter to the database
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter added successfully!', 'success')  # All good, let's roll
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            # Something went wrong, so undo changes
            db.session.rollback()
            flash(f'Error adding chapter: {e}', 'danger')

    form = ChapterForm()
    # Adding subject options to the dropdown in the form
    form.subject_id.choices = [(subject.id, subject.name) for subject in subjects]  
    return render_template('add_chapter.html', form=form)


# Route to edit an existing chapter
@chap_bp.route('/admin/edit_chapter/edit/<int:id>', methods=['GET', 'POST'])
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)  # Get the chapter or show a 404
    form = ChapterForm(obj=chapter)  # Pre-fill form with current data

    # When the form is submitted
    if request.method == 'POST':  
        # Update chapter details
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        db.session.commit()
        flash('Chapter updated successfully!', 'success')  # Boom, update done
        return redirect(url_for('admin_dashboard'))  # Back to the dashboard

    return render_template('edit_chapter.html', form=form, chapter=chapter)


# Route to delete a chapter
@chap_bp.route('/admin/delete_chapter/<int:id>', methods=['POST'])
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)  # Get the chapter or show a 404
    db.session.delete(chapter)  # Delete it from the database
    db.session.commit()  # Save the changes
    flash('Chapter deleted!', 'success')  # Bye-bye chapter
    return redirect(url_for('admin_dashboard'))  # Back to dashboard
