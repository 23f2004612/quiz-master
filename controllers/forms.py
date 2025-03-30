
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import DateField, PasswordField, StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    # Form for user login with role selection
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])  # Username with validation
    password = PasswordField('Password', validators=[DataRequired()])  # Password field
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])  # Role dropdown
    submit = SubmitField('Login')  # Submit button for login

class RegisterForm(FlaskForm):
    # Form for user registration
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])  # Username with validation
    password = PasswordField('Password', validators=[DataRequired()])  # Password field
    name = StringField('Full Name', validators=[DataRequired()])  # Full name of the user
    qualification = StringField('Qualification')  # Optional qualification field
    dob = DateField('Date of Birth', format='%Y-%m-%d')  # Date of birth in YYYY-MM-DD format
    submit = SubmitField('Register')  # Submit button for registration

class SubjectForm(FlaskForm):
    # Form for adding a subject
    name = StringField('Subject Name', validators=[DataRequired()])  # Name of the subject
    description = TextAreaField('Description')  # Subject description
    submit = SubmitField('Add Subject')  # Submit button for adding subject

class ChapterForm(FlaskForm):
    # Form for adding a chapter to a subject
    name = StringField('Chapter Name', validators=[DataRequired()])  # Name of the chapter
    description = TextAreaField('Description')  # Chapter description
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])  # Dropdown for subject selection
    submit = SubmitField('Save')  # Submit button for saving chapter

class QuizForm(FlaskForm):
    # Form for creating a quiz
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])  # Select chapter
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])  # Date input for quiz
    duration = IntegerField('Duration (Minutes)', validators=[DataRequired()])  # Duration of the quiz
    submit = SubmitField('Add Quiz')  # Submit button for adding quiz

class QuestionForm(FlaskForm):
    # Form for adding questions to a quiz
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])  # Select chapter
    quiz_id = SelectField('Quiz', coerce=int, validators=[DataRequired()])  # Select quiz
    title = StringField('Question Title', validators=[DataRequired()])  # Title of the question
    statement = TextAreaField('Question Statement', validators=[DataRequired()])  # Detailed question statement
    option1 = StringField('Option 1', validators=[DataRequired()])  # Option 1 for the question
    option2 = StringField('Option 2', validators=[DataRequired()])  # Option 2 for the question
    option3 = StringField('Option 3', validators=[DataRequired()])  # Option 3 for the question
    option4 = StringField('Option 4', validators=[DataRequired()])  # Option 4 for the question
    correct_option = SelectField('Correct Option', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], validators=[DataRequired()])  # Dropdown to select the correct option
    submit = SubmitField('Add Question')  # Submit button for adding question
