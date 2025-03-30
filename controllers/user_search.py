
from flask import app, render_template, request,Blueprint
from flask_login import current_user, login_required

from models.models import Chapter, Quiz, Score, Subject,db

user_search = Blueprint("user_search", __name__)

@user_search.route("/user/search_quiz", methods=['GET', 'POST'])
@login_required
def search_quiz():
    subjects = Subject.query.all()  # Get all available subjects for the dropdown
    chapters = Chapter.query.all()  # Get all available chapters for the dropdown
    quizzes = Quiz.query.all()  # Fetch all quizzes initially

    # Retrieve all quiz attempts made by the current user
    quiz_attempts = Score.query.filter_by(user_id=current_user.id).all()
    attempted_quiz_ids = [attempt.quiz_id for attempt in quiz_attempts]  # List of attempted quiz IDs

    # Handle search form submission
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')  # Get selected subject ID from the form
        chapter_id = request.form.get('chapter_id')  # Get selected chapter ID from the form

        # Filter quizzes based on subject and chapter
        if subject_id:
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject_id).all()  # Filter by subject
        if chapter_id:
            quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()  # Filter by chapter

    quiz_data = []  # Store quiz details to render in the template
    for quiz in quizzes:
        chapter = quiz.chapter  # Get chapter linked to the quiz
        subject_name = chapter.subject.name if chapter and chapter.subject else "Unknown"  # Fetch subject name
        chapter_name = chapter.name if chapter else "Unknown"  # Fetch chapter name

        # Check if the quiz is attempted and get the user's score if available
        is_attempted = quiz.id in attempted_quiz_ids
        score = None

        if is_attempted:
            attempt = next((attempt for attempt in quiz_attempts if attempt.quiz_id == quiz.id), None)  # Fetch the attempt data
            if attempt:
                score = attempt.score  # Get the score if the attempt exists

        # Append quiz information to the list
        quiz_data.append({
            "id": quiz.id,
            "subject_name": subject_name,
            "chapter_name": chapter_name,
            "date": quiz.date.strftime('%Y-%m-%d'),  # Format date
            "attempted": is_attempted,
            "score": score
        })

    # Pass subjects, chapters, and quiz data to the template
    return render_template("search_quiz.html", subjects=subjects, chapters=chapters, quizzes=quiz_data)
