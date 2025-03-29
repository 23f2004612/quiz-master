
from flask import app, render_template, request,Blueprint
from flask_login import login_required

from models.models import Chapter, Question, Quiz,Subject, User

admin_search = Blueprint("admin_search", __name__)

@admin_search.route("/admin/search", methods=["GET", "POST"])
@login_required
def admin_search_page():
     
    users = None
    subjects = None
    quizzes = None
    questions = None

    if request.method == 'POST':
        search_type = request.form.get('search_type')  # 'users', 'subjects', 'quizzes', 'questions'
        query = request.form.get('query')

        if search_type == 'users':
            if query:
                users = User.query.filter(User.username.ilike(f'%{query.lower()}%'), User.role == 'user').all()
                # If no users are found, we pass an empty list
                if not users:
                    users = []
            else:
                users = User.query.filter(User.role == 'user').all()

        elif search_type == 'subjects':
            if query:
                subjects = Subject.query.filter(Subject.name.ilike(f'%{query.lower()}%')).all()
            else:
                subjects = Subject.query.all()

        elif search_type == 'quizzes':
            if query:
                subject = Subject.query.filter(Subject.name.ilike(f'%{query.lower()}%')).first()
                if subject:
                    quizzes = Quiz.query.filter(Quiz.subject_id == subject.id).all()
                else:
                    quizzes = []  # No quizzes found if the subject doesn't exist
            else:
                quizzes = Quiz.query.all()

        elif search_type == 'questions':
            if query:
                questions = Question.query.join(Chapter).filter(Chapter.name.ilike(f'%{query.lower()}%')).all()
            else:
                questions = Question.query.all()

    return render_template('admin_search.html', users=users, subjects=subjects, quizzes=quizzes, questions=questions)
