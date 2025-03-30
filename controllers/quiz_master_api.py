
from flask import Flask
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.models import User, ActiveSession, Subject, Chapter, Quiz, Question, Score

app = Flask(__name__)
ma = Marshmallow(app)

spec = APISpec(
    title="Quizmaster API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[MarshmallowPlugin()]
)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class ActiveSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActiveSession
        load_instance = True

class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subject
        load_instance = True

class ChapterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chapter
        load_instance = True

class QuizSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quiz
        load_instance = True

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        load_instance = True

class ScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        load_instance = True

spec.components.schema("User", schema=UserSchema)
spec.components.schema("ActiveSession", schema=ActiveSessionSchema)
spec.components.schema("Subject", schema=SubjectSchema)
spec.components.schema("Chapter", schema=ChapterSchema)
spec.components.schema("Quiz", schema=QuizSchema)
spec.components.schema("Question", schema=QuestionSchema)
spec.components.schema("Score", schema=ScoreSchema)

@app.route("/users", methods=["GET"])
def get_users():
    """Get all users
    ---
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: array
              items: 
                $ref: '#/components/schemas/User'
    """
    return "Users route"

@app.route("/subjects", methods=["GET"])
def get_subjects():
    """Get all subjects
    ---
    responses:
      200:
        description: List of subjects
        content:
          application/json:
            schema:
              type: array
              items: 
                $ref: '#/components/schemas/Subject'
    """
    return "Subjects route"

@app.route("/chapters", methods=["GET"])
def get_chapters():
    """Get all chapters
    ---
    responses:
      200:
        description: List of chapters
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Chapter'
    """
    return "Chapters route"

@app.route("/quizzes", methods=["GET"])
def get_quizzes():
    """Get all quizzes
    ---
    responses:
      200:
        description: List of quizzes
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Quiz'
    """
    return "Quizzes route"

@app.route("/questions", methods=["GET"])
def get_questions():
    """Get all questions
    ---
    responses:
      200:
        description: List of questions
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Question'
    """
    return "Questions route"

@app.route("/scores", methods=["GET"])
def get_scores():
    """Get all scores
    ---
    responses:
      200:
        description: List of scores
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Score'
    """
    return "Scores route"


with open("quizmaster_openapi.yaml", "w") as f:
    f.write(spec.to_yaml())

print("OpenAPI YAML file generated as quizmaster_openapi.yaml")
