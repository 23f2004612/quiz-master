from flask import Blueprint, jsonify
from models.models import Subject, Chapter, Quiz, Score

api = Blueprint('api', __name__)

@api.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{'id': subject.id, 'name': subject.name, 'description': subject.description} for subject in subjects])

@api.route('/subjects/<int:id>', methods=['GET'])
def get_subject(id):
    subject = Subject.query.get(id)
    if subject:
        return jsonify({'id': subject.id, 'name': subject.name, 'description': subject.description})
    return jsonify({'message': 'Subject not found'}), 404

@api.route('/chapters', methods=['GET'])
def get_chapters():
    chapters = Chapter.query.all()
    return jsonify([{'id': chapter.id, 'name': chapter.name, 'description': chapter.description, 'subject_id': chapter.subject_id} for chapter in chapters])

@api.route('/chapters/<int:id>', methods=['GET'])
def get_chapter(id):
    chapter = Chapter.query.get(id)
    if chapter:
        return jsonify({'id': chapter.id, 'name': chapter.name, 'description': chapter.description, 'subject_id': chapter.subject_id})
    return jsonify({'message': 'Chapter not found'}), 404

@api.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{'id': quiz.id, 'chapter_id': quiz.chapter_id, 'subject_id': quiz.subject_id, 'date': quiz.date, 'duration': quiz.duration} for quiz in quizzes])

@api.route('/quizzes/<int:id>', methods=['GET'])
def get_quiz(id):
    quiz = Quiz.query.get(id)
    if quiz:
        return jsonify({'id': quiz.id, 'chapter_id': quiz.chapter_id, 'subject_id': quiz.subject_id, 'date': quiz.date, 'duration': quiz.duration})
    return jsonify({'message': 'Quiz not found'}), 404

@api.route('/scores', methods=['GET'])
def get_scores():
    scores = Score.query.all()
    return jsonify([{'id': score.id, 'user_id': score.user_id, 'quiz_id': score.quiz_id, 'score': score.score, 'total_questions': score.total_questions, 'date_attempted': score.date_attempted} for score in scores])

@api.route('/scores/<int:id>', methods=['GET'])
def get_score(id):
    score = Score.query.get(id)
    if score:
        return jsonify({'id': score.id, 'user_id': score.user_id, 'quiz_id': score.quiz_id, 'score': score.score, 'total_questions': score.total_questions, 'date_attempted': score.date_attempted})
    return jsonify({'message': 'Score not found'}), 404
