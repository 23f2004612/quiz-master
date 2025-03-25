
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from forms import QuizForm
from models import Chapter, Question, Quiz,db

quiz_bp = Blueprint("quiz_auth", __name__)

@quiz_bp.route('/admin/quizzes')
def list_quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

@quiz_bp.route('/admin/add_quiz', methods=['GET', 'POST'])
def add_quiz():

    form = QuizForm()
    form.chapter_id.choices = [(chapter.id, chapter.name) for chapter in Chapter.query.all()]

    if request.method == 'POST':  # Check if form is submitted
        chapter_id = request.form.get('chapter_id')
        date_str = request.form.get('date')
        duration = request.form.get('duration')

        if not chapter_id or not date_str or not duration:
            flash('All fields are required!', 'danger')
            return render_template('add_quiz.html', form=form)


        try:
            quiz_date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert to datetime
            chapter = Chapter.query.get(int(chapter_id))  # Get subject from chapter

            if not chapter:
                flash('Invalid chapter selection.', 'danger')
                return render_template('add_quiz.html', form=form)

            quiz = Quiz(
                chapter_id=int(chapter_id),
                subject_id=chapter.subject_id,
                date=quiz_date,
                duration=int(duration)
            )

            db.session.add(quiz)
            db.session.commit()
            flash('Quiz added successfully!', 'success')
            return redirect(url_for('quiz_auth.list_quizzes'))

        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')

    return render_template('add_quiz.html', form=form)


@quiz_bp.route('/admin/edit_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(id):
    quiz = Quiz.query.get(id)
    if not quiz:
        flash('Quiz not found!', 'error')
        return redirect(url_for('quiz_auth.list_quizzes'))

    form = QuizForm(obj=quiz)  

    if request.method == 'POST':  
        quiz.chapter_id = request.form['chapter_id']
        quiz.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        quiz.duration = request.form['duration']

        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('quiz_auth.list_quizzes'))  

    return render_template('edit_quiz.html', form=form, quiz=quiz, chapters=Chapter.query.all())


@quiz_bp.route('/admin/quiz/delete', methods=['POST'])
def delete_quiz():
    quiz_id = request.form.get('quiz_id')
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        
        Question.query.filter_by(quiz_id=quiz.id).delete()

    # Now delete the quiz
        db.session.delete(quiz)
        db.session.commit()

        flash('Quiz deleted successfully!', 'success')
        return redirect(url_for('quiz_auth.list_quizzes'))
    
    return render_template('delete_quiz.html', quiz=quiz)
