
from controllers.user_search import user_search
import plotly.graph_objs as go
from flask import app, render_template,Blueprint
from flask_login import current_user, login_required
from models.models import Question, Quiz, Score, Subject, User

admin_sum = Blueprint("admin_sum", __name__)

@admin_sum.route('/admin/summary')
@login_required

def admin_summary():
    # Initialize counters and lists for performance analysis
    pass_count = 0
    fail_count = 0
    user_avg_scores = []  # Store average scores of users
    user_names = []  # Store names of users

    # Fetch all scores and users from the database
    all_scores = Score.query.all()
    all_users = User.query.filter(User.role == 'user').all()

    # Loop through each user to calculate their performance
    for user in all_users:
        scores = Score.query.filter_by(user_id=user.id).all()
        total_questions_attempted = 0
        total_correct_answers = 0

        # Loop through each quiz taken by the user
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)  # Get quiz details
            questions = Question.query.filter_by(quiz_id=score.quiz_id).all()  # Fetch questions in the quiz

            total_questions = len(questions)  # Count total questions in the quiz
            total_questions_attempted += total_questions  # Accumulate questions attempted
            total_correct_answers += score.score  # Accumulate user's correct answers

        # Calculate the average score if questions were attempted
        if total_questions_attempted > 0:
            avg_score = (total_correct_answers / total_questions_attempted) * 100
        else:
            avg_score = 0  # No questions attempted means 0% score

        user_avg_scores.append(avg_score)  # Store average score
        user_names.append(user.name)  # Store user name

        # Check if the user passed based on the latest quiz score
        if scores:
            last_score = scores[-1]  # Get the latest score
            quiz = Quiz.query.get(last_score.quiz_id)
            questions = Question.query.filter_by(quiz_id=last_score.quiz_id).all()
            passing_score = len(questions) * 0.5  # Passing criteria (50% correct)
            if last_score.score >= passing_score:
                pass_count += 1  # User passed
            else:
                fail_count += 1  # User failed

    # Create visualizations using Plotly
    pie_data = go.Pie(labels=['Pass', 'Fail'], values=[pass_count, fail_count])
    pie_layout = go.Layout(title="Quiz Performance (Pass vs Fail)")

    bar_data = go.Bar(x=user_names, y=user_avg_scores)
    bar_layout = go.Layout(title="Average Score per User")

    pie_chart = go.Figure(data=[pie_data], layout=pie_layout)  # Pie chart for pass/fail
    bar_chart = go.Figure(data=[bar_data], layout=bar_layout)  # Bar chart for user scores

    # Generate HTML for charts
    pie_chart_html = pie_chart.to_html(full_html=False)
    bar_chart_html = bar_chart.to_html(full_html=False)

    # Render the admin summary template with charts
    return render_template('admin_summary.html', pie_chart=pie_chart_html, bar_chart=bar_chart_html)
