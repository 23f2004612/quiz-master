
from flask import app, render_template, request,Blueprint
from flask_login import current_user, login_required

from models.models import Chapter, Quiz, Score, Subject,db

user_search = Blueprint("user_search", __name__)

@user_search.route("/user/search_quiz", methods=['GET', 'POST'])
@login_required
def search_quiz():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()

    quiz_attempts = Score.query.filter_by(user_id=current_user.id).all()
    attempted_quiz_ids = [attempt.quiz_id for attempt in quiz_attempts]

    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        chapter_id = request.form.get('chapter_id')

        if subject_id:
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject_id).all()
        if chapter_id:
            quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    quiz_data = []
    for quiz in quizzes:
        chapter = quiz.chapter
        subject_name = chapter.subject.name if chapter and chapter.subject else "Unknown"
        chapter_name = chapter.name if chapter else "Unknown"

        is_attempted = quiz.id in attempted_quiz_ids
        score = None

        if is_attempted:
            attempt = next((attempt for attempt in quiz_attempts if attempt.quiz_id == quiz.id), None)
            if attempt:
                score = attempt.score    

        quiz_data.append({
            "id": quiz.id,
            "subject_name": subject_name,
            "chapter_name": chapter_name,
            "date": quiz.date.strftime('%Y-%m-%d'),
            "attempted": is_attempted,
            "score": score
        })

    return render_template("search_quiz.html",subjects=subjects, chapters=chapters, quizzes=quiz_data)
