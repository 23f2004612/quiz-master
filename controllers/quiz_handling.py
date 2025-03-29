from flask import app, flash, redirect, render_template, request, session, url_for,Blueprint
from flask_login import current_user, login_required
from sqlalchemy import func
from models.models import Question, Quiz, Score,db

quiz_handle_auth = Blueprint("quiz_handle_auth", __name__)

@quiz_handle_auth.route('/user/view_quiz/<int:id>', methods=['GET'])
@login_required
def view_quiz(id):
    quiz = Quiz.query.get(id)
    if not quiz:
        flash('Quiz not found!', 'error')
        return redirect(url_for('user_dashboard'))  # Redirect to dashboard if quiz is not found
    
    chapter = quiz.chapter
    subject = chapter.subject if chapter else None
    question_count = Question.query.filter_by(quiz_id=quiz.id).count()

    quiz_details = {
        "id": quiz.id,
        "chapter_name": chapter.name if chapter else "Unknown",
        "subject_name": subject.name if subject else "Unknown",
        "date": quiz.date.strftime('%Y-%m-%d'),
        "duration": quiz.duration,
        "num_questions": question_count
    }

    return render_template("view_quiz.html", quiz=quiz_details)

@quiz_handle_auth.route('/start_quiz/<int:quiz_id>/<int:question_index>', methods=['GET', 'POST'])
@login_required

def start_quiz(quiz_id, question_index):
    quiz = Quiz.query.get_or_404(quiz_id)  
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if not questions:
        flash("No questions available for this quiz.", "danger")
        return redirect(url_for('user_dashboard'))

    if question_index < 0 or question_index >= len(questions):
        flash("Invalid question index.", "danger")
        return redirect(url_for('user_dashboard'))  

    question = questions[question_index]

    if request.method == 'POST':
        
        user_answer = request.form.get('answer') # Will raise KeyError if 'answer' is not found

        print(f"Retrieved user's answer for Q{question_index + 1}: {user_answer}") 

        if user_answer:
            # Store answer in session or database (optional)
            session[f'quiz_{quiz_id}_q{question_index}'] = user_answer
            print(f"Retrieved Q{question_index + 1}: {user_answer}")
        
        # Redirect to next question or submit
        if question_index + 1 < len(questions):
            return redirect(url_for('quiz_handle_auth.start_quiz', quiz_id=quiz_id, question_index=question_index + 1))
        else:
            return redirect(url_for('quiz_handle_auth.submit_quiz', quiz_id=quiz_id))

    return render_template('start_quiz.html', quiz=quiz, question=question, question_index=question_index, total=len(questions))

@quiz_handle_auth.route('/submit_quiz/<int:quiz_id>', methods=['GET','POST'])
@login_required

def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    total_score = 0
    correct_answers = 0
    feedback_list = []

    print(f"Submitting Quiz ID: {quiz.id}")
    print(f"Total Questions: {len(questions)}")

    for question_index, question in enumerate(questions):   
        user_answer = session.get(f'quiz_{quiz_id}_q{question_index}')
        print(f"Retrieved user's answer for Q{question_index + 1}: {user_answer}")
        
        if user_answer and user_answer == question.correct_option:  # Assuming question.correct_answer holds the correct answer
            correct_answers += 1
            feedback_list.append(f"Question {question.id}: Correct!")
        else:
            feedback_list.append(f"Question {question.id}: Incorrect! The correct answer was {question.correct_option}.")

    total_score = correct_answers 

    quiz_attempt = Score(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=total_score,
        total_questions=len(questions)
    )
    db.session.add(quiz_attempt)
    db.session.commit()

    session['quiz_feedback'] = feedback_list
    session['total_score'] = total_score
    session['total_questions'] = len(questions)

    print(f"Total score: {total_score} / {len(questions)}")
    for question_index in range(len(questions)):
        session.pop(f'quiz_{quiz_id}_q{question_index}', None)
    
    return redirect(url_for('quiz_handle_auth.scores',quiz_id=quiz.id))
    

@quiz_handle_auth.route('/scores', methods=['GET','POST'])
@login_required
def scores(): 
    
    quiz_id = request.args.get('quiz_id') 
    feedback_list = session.pop('quiz_feedback', [])  
    total_score = session.pop('total_score', 0)  
    total_questions = session.pop('total_questions', 0) 

    quiz_attempts = Score.query.filter_by(user_id=current_user.id).all()

    # Prepare data for the quiz attempts summary
    quiz_summary_data = []
    for attempt in quiz_attempts:

        quiz = Quiz.query.get(attempt.quiz_id)
        if quiz and quiz.chapter:

            chapter = quiz.chapter
            subject = chapter.subject

            quiz_summary_data.append({

                "subject_name": subject.name if subject else "Unknown",
                "chapter_name": chapter.name if chapter else "Unknown",
                "date_attempted": attempt.date_attempted.strftime('%Y-%m-%d') if attempt.date_attempted else "N/A",
                "duration": quiz.duration,
                "total_questions": attempt.total_questions,
                "score": attempt.score
            })

    total_attempted_quizzes = len(quiz_attempts)

    # Calculate average score (assuming you already have the score for each quiz attempt)
    total_score = db.session.query(func.sum(Score.score)).filter_by(user_id=current_user.id).scalar() or 0
    total_questions = db.session.query(func.sum(Score.total_questions)).filter_by(user_id=current_user.id).scalar() or 0
    average_score = (total_score / total_questions) * 100 if total_questions > 0 else 0

    
    return render_template('scores.html',attempts=quiz_summary_data,total_attempted_quizzes=total_attempted_quizzes,
                           average_score=average_score,total_score=total_score, 
                           total_questions=total_questions,
                           feedback_list=feedback_list)
