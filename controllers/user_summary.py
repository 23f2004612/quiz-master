
from controllers.user_search import user_search
import plotly.graph_objs as go
from flask import app, render_template,Blueprint
from flask_login import current_user, login_required
from models.models import Question, Quiz, Score, Subject

user_sum = Blueprint("user_sum", __name__)

@user_sum.route('/user/summary')
@login_required  
def user_summary():
    user_id = current_user.id  # Get the ID of the currently logged-in user
    scores = Score.query.filter_by(user_id=user_id).all()  # Fetch all scores for this user

    pass_count = 0
    fail_count = 0
    subject_data = {}  # Dictionary to store performance by subject

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)  # Get the quiz associated with the score
        subject = Subject.query.get(quiz.subject_id)  # Get the subject for the quiz
        questions = Question.query.filter_by(quiz_id=score.quiz_id).all()  # Fetch all questions for the quiz

        total_weightage = len(questions)  # Total number of questions
        passing_score = total_weightage * 0.5  # Calculate passing score (50%)

        # Determine pass or fail
        if score.score >= passing_score:
            pass_count += 1
        else:
            fail_count += 1

        # Track performance for each subject
        if subject.id in subject_data:
            subject_data[subject.id]['total_percentage'] += (score.score / total_weightage) * 100
            subject_data[subject.id]['quiz_count'] += 1
        else:
            subject_data[subject.id] = {'total_percentage': (score.score / total_weightage) * 100, 'quiz_count': 1}

    # Prepare data for charts
    pie_data = go.Pie(labels=['Pass', 'Fail'], values=[pass_count, fail_count])

    subject_names = []
    avg_percentages = []

    # Calculate average percentages for each subject
    for subject_id, data in subject_data.items():
        avg_percentage = data['total_percentage'] / data['quiz_count']
        subject_names.append(Subject.query.get(subject_id).name)
        avg_percentages.append(avg_percentage)

    bar_data = go.Bar(x=subject_names, y=avg_percentages)

    # Chart layouts
    pie_layout = go.Layout(title="Quiz Performance (Pass vs Fail)")
    bar_layout = go.Layout(title="Average Percentage per Subject")

    pie_chart = go.Figure(data=[pie_data], layout=pie_layout)
    bar_chart = go.Figure(data=[bar_data], layout=bar_layout)

    pie_chart_html = pie_chart.to_html(full_html=False)
    bar_chart_html = bar_chart.to_html(full_html=False)

    return render_template('user_summary.html', pie_chart=pie_chart_html, bar_chart=bar_chart_html)
