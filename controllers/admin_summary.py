
from controllers.user_search import user_search
import plotly.graph_objs as go
from flask import app, render_template,Blueprint
from flask_login import current_user, login_required
from models.models import Question, Quiz, Score, Subject, User

admin_sum = Blueprint("admin_sum", __name__)

@admin_sum.route('/admin/summary')
@login_required
def admin_summary():
    
    pass_count = 0
    fail_count = 0
    user_avg_scores = []
    user_names = []

    all_scores = Score.query.all()
    all_users = User.query.filter(User.role == 'user').all()

    for user in all_users:
        scores = Score.query.filter_by(user_id=user.id).all()
        total_questions_attempted = 0
        total_correct_answers = 0

        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            questions = Question.query.filter_by(quiz_id=score.quiz_id).all()

            total_questions = len(questions)
            total_questions_attempted += total_questions
            total_correct_answers += score.score

        if total_questions_attempted > 0:
            avg_score = (total_correct_answers / total_questions_attempted) * 100
        else:
            avg_score = 0

        user_avg_scores.append(avg_score)
        user_names.append(user.name)

        # Calculate the passing score based on the last quiz for the user
        if scores:
            last_score = scores[-1]
            quiz = Quiz.query.get(last_score.quiz_id)
            questions = Question.query.filter_by(quiz_id=last_score.quiz_id).all()
            passing_score = len(questions) * 0.5
            if last_score.score >= passing_score:
                pass_count += 1
            else:
                fail_count += 1

    pie_data = go.Pie(labels=['Pass', 'Fail'], values=[pass_count, fail_count])
    pie_layout = go.Layout(title="Quiz Performance (Pass vs Fail)")

    bar_data = go.Bar(x=user_names, y=user_avg_scores)
    bar_layout = go.Layout(title="Average Score per User")

    pie_chart = go.Figure(data=[pie_data], layout=pie_layout)
    bar_chart = go.Figure(data=[bar_data], layout=bar_layout)

    pie_chart_html = pie_chart.to_html(full_html=False)
    bar_chart_html = bar_chart.to_html(full_html=False)

    return render_template('admin_summary.html', pie_chart=pie_chart_html, bar_chart=bar_chart_html)
