import random

from flask import (
    Flask,
    request,
    abort,
    jsonify)
from flask_cors import CORS

from backend.models import (
    setup_db,
    Question,
    Category)

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        return response

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        items = [item.format() for item in selection]
        current_items = items[start:end]

        return current_items

    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.all()
        categories = [category.format() for category in selection]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'categories': categories,
        }), 200

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()

        questions = paginate_questions(request, selection)
        current_category = [question['category'] for question in questions]
        current_category = list(set(current_category))
        categories = [cat.format() for cat in Category.query.all()]

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': current_category,
        }), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if not question:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            }), 200

        except Exception as e:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def add_question():

        try:
            data = request.json
            to_add = Question(data['question'],
                              data['answer'],
                              data['category'],
                              data['difficulty']
                              )
            to_add.insert()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            search_term = request.json['searchTerm']

            selection = Question.query.filter(
                Question.question.ilike('%' + search_term + '%')).all()

            search_results = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': search_results,
                'total_questions': len(search_results),
                'current_category': None
            }), 200
        except Exception as e:
            abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': len(selection),
            'current_category': category_id,
        })

    @app.route("/quizzes", methods=['POST'])
    def quizzes():
        previous_questions = request.json.get('previous_questions')
        quiz_category = request.json.get('quiz_category')

        if previous_questions is None or quiz_category is None:
            abort(404)

        if quiz_category['id'] == 0:  # all categories
            questions_by_category = Question.query. \
                filter(Question.id.notin_(previous_questions)). \
                all()

        else:  # specific category
            questions_by_category = Question.query. \
                filter_by(category=quiz_category['id']). \
                filter(Question.id.notin_(previous_questions)). \
                all()

        if questions_by_category:
            formatted_questions = \
                [question.format() for question in questions_by_category]
            return jsonify({'question': formatted_questions[0]}), 200
        else:
            return jsonify({'question': False}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app
