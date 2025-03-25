
from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms import ChapterForm
from models import Chapter, Subject,db

chap_bp = Blueprint("chap_auth", __name__)

@chap_bp.route('/admin/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    subjects = Subject.query.all()  # Fetch all subjects

    if not subjects:  
        flash("No subjects available. Please create a subject first.", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':  # Handle form submission
        name = request.form['name']
        description = request.form['description']
        subject_id = request.form['subject_id']

        # Create a new chapter instance
        chapter = Chapter(
            name=name,
            description=description,
            subject_id=subject_id
        )

        try:
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error adding chapter: {e}', 'danger')

    form = ChapterForm()
    form.subject_id.choices = [(subject.id, subject.name) for subject in subjects]  # Assign choices
    return render_template('add_chapter.html', form=form)


@chap_bp.route('/admin/edit_chapter/edit/<int:id>', methods=['GET', 'POST'])
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)

    if request.method == 'POST':  # Handle form submission
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))  # Redirect back after saving

    return render_template('edit_chapter.html', form=form, chapter=chapter)

@chap_bp.route('/admin/delete_chapter/<int:id>', methods=['POST'])

def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


