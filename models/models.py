
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


'''
User Model
Represents users in the system, storing details like username, password, name, qualification, date of birth, and role.
Provides authentication and role-based access.'
'''

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)  # `id` is now the primary key
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=True)  # Date of Birth
    role = db.Column(db.String(20), nullable=False, default='user')

'''
ActiveSession Model
Tracks active user sessions with timestamps and roles.
Used for session management and monitoring.

'''
class ActiveSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='active_sessions', lazy=True)

"""
Subject & Chapter Models

Organizes subjects and their related chapters.
Establishes a one-to-many relationship between subjects and chapters.
"""

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapters = db.relationship('Chapter', backref='subject', lazy=True,cascade="all, delete-orphan")

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    questions = db.relationship('Question', backref='chapter', lazy=True)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

'''
Quiz Model
Represents quizzes linked to specific subjects and chapters.
Stores quiz details such as date, duration, and questions associated.
'''
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', name="fk_quiz_chapter"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', name="fk_quiz_subject"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)


'''
Question Model
Stores questions, options, and the correct answer.
Linked to specific quizzes and chapters.
'''
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

'''
Score Model
Stores quiz results for each user, including score, total questions, and date attempted.
Facilitates score tracking and quiz performance analysis.

'''
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    date_attempted = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('scores', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))

    def __repr__(self):
        return f'<Score {self.id} - {self.score}>'


