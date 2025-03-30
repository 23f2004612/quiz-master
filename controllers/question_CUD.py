
from flask import Blueprint, flash, redirect, render_template, request, url_for
from controllers.forms import QuestionForm
from models.models import Chapter, Question, Quiz,db

ques_bp = Blueprint("ques_auth", __name__)


@ques_bp.route('/admin/add_question', methods=['GET', 'POST'])
def add_question():

    chapter_id = request.args.get('chapter_id')  # Getting the chapter ID from the URL
    quiz_id = request.args.get('quiz_id')  # Getting the quiz ID from the URL

    # Check if both chapter_id and quiz_id are provided
    if not chapter_id or not quiz_id:
        flash('Invalid access to question form.', 'danger')  # Error if missing IDs
        return redirect(url_for('quiz_auth.list_quizzes'))  # Redirect if IDs are missing

    form = QuestionForm()  # Creating a form instance

    if request.method == 'POST':  # Checking if the request is POST (form submission)

        # Manual validation for all form fields (since validate_on_submit is skipped)
        if not form.title.data or not form.statement.data or \
           not form.option1.data or not form.option2.data or \
           not form.option3.data or not form.option4.data or \
           not form.correct_option.data:
            flash('All fields are required!', 'danger')  # Error if any field is empty
            return render_template('admin_questions.html', form=form, chapter_id=chapter_id, quiz_id=quiz_id)  # Re-render form

        try:
            chapter = Chapter.query.get(int(chapter_id))  # Fetching chapter by ID
            quiz = Quiz.query.get(int(quiz_id))  # Fetching quiz by ID

            # Validate chapter and quiz existence
            if not chapter or not quiz:
                flash('Invalid chapter or quiz.', 'danger')  # Error if invalid
                return redirect(url_for('quiz_auth.list_quizzes'))  # Redirect on error

            # Creating a question instance
            question = Question(
                chapter_id=int(chapter_id),
                quiz_id=int(quiz_id),
                title=request.form.get('title'),
                statement=request.form.get('statement'),
                option1=request.form.get('option1'),
                option2=request.form.get('option2'),
                option3=request.form.get('option3'),
                option4=request.form.get('option4'),
                correct_option=request.form.get('correct_option')
            )

            # Adding and committing question to the database
            db.session.add(question)
            db.session.commit()
            flash('Question added successfully!', 'success')  # Success message
            return redirect(url_for('quiz_auth.list_quizzes', chapter_id=chapter_id))

        except ValueError:
            flash('Invalid data format.', 'danger')  # Error if invalid data format

    # Render the question form template if GET request or validation fails
    return render_template('admin_questions.html', form=form, chapter_id=chapter_id, quiz_id=quiz_id)


@ques_bp.route('/admin/question/edit/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    question = Question.query.get_or_404(id)  # Fetch the question or return 404
    form = QuestionForm(obj=question)  # Pre-fill the form with question data
    form.chapter_id.choices = [(chapter.id, chapter.name) for chapter in Chapter.query.all()]  # Populate dropdown

    if request.method == 'POST':  # Checking if POST request
        title = request.form.get('title')
        statement = request.form.get('statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        # Manual validation
        if not title or not statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash('All fields are required!', 'danger')
            return render_template('edit_question.html', form=form, question=question)

        try:
            # Updating the question details
            question.title = title
            question.statement = statement
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.correct_option = correct_option

            db.session.commit()  # Save changes to DB
            flash('Question updated successfully!', 'success')
            return redirect(url_for('quiz_auth.list_quizzes', chapter_id=question.chapter_id))

        except Exception as e:
            flash('Error updating question.', 'danger')
            return render_template('edit_question.html', form=form, question=question)

    return render_template('edit_question.html', form=form, question=question)


@ques_bp.route('/admin/question/delete', methods=['POST'])
def delete_question():

    question_id = request.form.get('question_id')  # Get question ID from form
    question = Question.query.get_or_404(question_id)  # Fetch or return 404

    # Delete the question
    db.session.delete(question)
    db.session.commit()  # Commit deletion

    flash('Question deleted successfully!', 'success')  # Success message
    return redirect(url_for('quiz_auth.list_quizzes'))
