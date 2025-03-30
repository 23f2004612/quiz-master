
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from controllers.forms import QuizForm
from models.models import Chapter, Question, Quiz,db

quiz_bp = Blueprint("quiz_auth", __name__)

@quiz_bp.route('/admin/quizzes')
def list_quizzes():
    quizzes = Quiz.query.all()  # Fetch all quizzes from the database
    return render_template('quizzes.html', quizzes=quizzes)  # Pass quizzes to the template

@quiz_bp.route('/admin/add_quiz', methods=['GET', 'POST'])
def add_quiz():

    form = QuizForm()  # Initialize the quiz form
    form.chapter_id.choices = [(chapter.id, chapter.name) for chapter in Chapter.query.all()]  # Populate chapter choices

    if request.method == 'POST':  # Check if form is submitted
        chapter_id = request.form.get('chapter_id')  # Get selected chapter ID
        date_str = request.form.get('date')  # Get quiz date as a string
        duration = request.form.get('duration')  # Get quiz duration

        if not chapter_id or not date_str or not duration:  # Ensure all fields are filled
            flash('All fields are required!', 'danger')
            return render_template('add_quiz.html', form=form)  # Reload form with error message

        try:
            quiz_date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert date string to datetime object
            chapter = Chapter.query.get(int(chapter_id))  # Fetch chapter by ID

            if not chapter:  # Validate chapter existence
                flash('Invalid chapter selection.', 'danger')
                return render_template('add_quiz.html', form=form)

            quiz = Quiz(
                chapter_id=int(chapter.id),
                subject_id=chapter.subject_id,  # Assign subject ID based on chapter
                date=quiz_date,
                duration=int(duration)  # Store duration as integer
            )

            db.session.add(quiz)  # Add quiz to database
            db.session.commit()  # Commit transaction
            flash('Quiz added successfully!', 'success')
            return redirect(url_for('quiz_auth.list_quizzes'))  # Redirect after success

        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')

    return render_template('add_quiz.html', form=form)  # Render form for GET request

@quiz_bp.route('/admin/edit_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(id):
    quiz = Quiz.query.get(id)  # Get quiz by ID
    if not quiz:  # Handle missing quiz
        flash('Quiz not found!', 'error')
        return redirect(url_for('quiz_auth.list_quizzes'))

    form = QuizForm(obj=quiz)  # Prefill form with quiz data

    if request.method == 'POST':  # Check if form is submitted
        quiz.chapter_id = request.form['chapter_id']  # Update chapter ID
        quiz.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()  # Update date
        quiz.duration = request.form['duration']  # Update duration

        db.session.commit()  # Commit updates
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('quiz_auth.list_quizzes'))  # Redirect after success

    return render_template('edit_quiz.html', form=form, quiz=quiz, chapters=Chapter.query.all())

@quiz_bp.route('/admin/quiz/delete', methods=['POST'])
def delete_quiz():
    quiz_id = request.form.get('quiz_id')  # Get quiz ID from form
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch quiz or 404 if not found

    if request.method == 'POST':  # Confirm deletion
        Question.query.filter_by(quiz_id=quiz.id).delete()  # Delete related questions

        db.session.delete(quiz)  # Delete the quiz itself
        db.session.commit()  # Commit deletion

        flash('Quiz deleted successfully!', 'success')
        return redirect(url_for('quiz_auth.list_quizzes'))  # Redirect to quiz list

    return render_template('delete_quiz.html', quiz=quiz)
