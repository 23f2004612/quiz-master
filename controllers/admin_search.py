
from flask import app, render_template, request,Blueprint
from flask_login import login_required

from models.models import Chapter, Question, Quiz,Subject, User

admin_search = Blueprint("admin_search", __name__)

@admin_search.route("/admin/search", methods=["GET", "POST"])
@login_required
def admin_search_page():
    # Initialize variables to store search results based on search type
    users = None
    subjects = None
    quizzes = None
    questions = None

    if request.method == 'POST':  # Check if the form was submitted
        search_type = request.form.get('search_type')  # Get the selected search type (users, subjects, quizzes, questions)
        query = request.form.get('query')  # Get the search query entered by the admin

        # Handle search for users
        if search_type == 'users':
            if query:
                users = User.query.filter(User.name.ilike(f'%{query.lower()}%'), User.role == 'user').all()  # Search for users matching query
                if not users:
                    users = []  # Return an empty list if no users found
            else:
                users = User.query.filter(User.role == 'user').all()  # Return all users if no query provided

        # Handle search for subjects
        elif search_type == 'subjects':
            if query:
                subjects = Subject.query.filter(Subject.name.ilike(f'%{query.lower()}%')).all()  # Search for subjects
            else:
                subjects = Subject.query.all()  # Return all subjects if no query provided

        # Handle search for quizzes
        elif search_type == 'quizzes':
            if query:
                subject = Subject.query.filter(Subject.name.ilike(f'%{query.lower()}%')).first()  # Search for matching subject
                if subject:
                    quizzes = Quiz.query.filter(Quiz.subject_id == subject.id).all()  # Get quizzes for subject
                else:
                    quizzes = []  # No quizzes found if subject doesn't exist
            else:
                quizzes = Quiz.query.all()  # Return all quizzes if no query provided

        # Handle search for questions
        elif search_type == 'questions':
            if query:
                questions = Question.query.join(Chapter).filter(Chapter.name.ilike(f'%{query.lower()}%')).all()  # Search by chapter name
            else:
                questions = Question.query.all()  # Return all questions if no query provided

    return render_template('admin_search.html', users=users, subjects=subjects, quizzes=quizzes, questions=questions)  # Pass search results to template
