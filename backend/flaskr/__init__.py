from flask import (
    Flask,
    abort,
    request,
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
    app.debug = True

    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,'
                                                             'Authorization,'
                                                             'true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,'
                                                             'DELETE,OPTIONS')
        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [cat.format() for cat in categories]
        return jsonify({
            'categories': formatted_categories
        }), 200

    @app.route("/questions", methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        if len(questions) == 0:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        formatted_categories = [cat.format() for cat in categories]

        curr_cat = [question['category'] for question in formatted_questions]
        current_category = list(set(curr_cat))
        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': current_category
        }), 200

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question_by_id(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify({'success': True}), 200

    @app.route("/questions", methods=['POST'])
    def add_questions():

        question = request.json.get('question')
        answer = request.json.get('answer')
        difficulty = request.json.get('difficulty')
        category = request.json.get('category')

        if question is None or answer is None:
            abort(422)

        Question(question, answer, category, difficulty).insert()

        return jsonify({'success': True}), 200

    @app.route('/search-questions', methods=["POST"])
    def search_questions():
        search_term = request.json.get('searchTerm')

        questions = Question.query.filter(
            Question.question.ilike('%' + search_term + '%')).all()

        len_questions = len(questions)

        if len_questions == 0:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        curr_cat = [question['category'] for question in formatted_questions]
        current_category = list(set(curr_cat))

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len_questions,
            'current_category': current_category
        }), 200

    @app.route("/categories/<int:cat_id>/questions")
    def get_by_category(cat_id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.filter_by(category=cat_id).all()
        if len(questions) == 0:
            abort(404)
        formatted_question = [question.format() for question in questions]

        response = jsonify({
            'questions': formatted_question[start:end],
            'total_questions': len(formatted_question),
            'current_category': cat_id
        })

        return response, 200

    @app.route("/quizzes", methods=['POST'])
    def quizzes():
        previous_questions = request.json.get('previous_questions')
        quiz_category = request.json.get('quiz_category')

        if quiz_category['id'] == 0:  # all categories
            questions_by_category = Question.query. \
                filter(Question.id.notin_(previous_questions)). \
                all()

        else:
            questions_by_category = Question.query. \
                filter_by(category=quiz_category['id']). \
                filter(Question.id.notin_(previous_questions)). \
                all()
        if questions_by_category:
            formatted_questions = \
                [question.format() for question in questions_by_category]
            return jsonify({'question': formatted_questions[0],
                            },
                           ), 200
        else:
            return jsonify({'question': False}), 200

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "not found"
        }), 404

    @app.errorhandler(422)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': error
        }), 404

    return app
