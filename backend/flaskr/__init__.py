import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    return questions[start:end]


def create_app():
    # Create and configure the app
    app = Flask(__name__)
    database_path = \
        'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(user="xxxxxxx",
                                                                        password="xxxx",
                                                                        host="xxxxxxxx",
                                                                        port=xxxx,
                                                                        db_name="xxxxxxxx")
    setup_db(app, database_path=database_path)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS,PUT')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {category.id: category.type for category in Category.query.order_by(Category.type).all()}
        if len(categories) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "categories": categories,
                "total_categories": len(categories)
            })

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
            if len(selection) == 0:
                abort(404)
            else:
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "totalQuestions": len(selection),
                    "currentCategory": Category.query.get(category_id).type
                })
        except:
            abort(404)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        categories = [category.type for category in Category.query.order_by(Category.id).all()]
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0 or len(categories) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "current_category": None,
            "categories": categories,
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            Question.query.get(question_id).delete()
            return jsonify({
                "success": True,
                "deleted": question_id
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_q_question = body.get("question", None)
        new_q_answer = body.get("answer", None)
        new_q_difficulty = body.get("difficulty", None)
        new_q_category_id = body.get("category", None)

        if int(new_q_category_id) not in [category.id for category in Category.query.order_by(Category.id).all()]:
            abort(400)

        if not new_q_question or not new_q_answer:
            abort(400)

        try:
            question = Question(question=new_q_question,
                                answer=new_q_answer,
                                category=new_q_category_id,
                                difficulty=new_q_difficulty)
            question.insert()

            return jsonify({
                "success": True,
                "created": question.id,
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()["searchTerm"]
        if not search_term:
            abort(404)
        try:
            questions = \
                [question.format() for question in Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()]
            return jsonify({
                "success": True,
                "questions": questions,
                "totalQuestions": len(questions),
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play():
        try:
            body = request.get_json()
            category_id = body["quiz_category"]["id"]
            category_name = body["quiz_category"]["type"]

            if category_name not in [category.format()["type"] for category in Category.query.all()]:
                questions_ids = set([question.format()["id"] for question in Question.query.all()])
            else:
                questions_ids = set(
                    [question.format()["id"] for question in Question.query.filter(Question.category == category_id)])

            previous_questions_ids = set(body["previous_questions"])

            try:
                selected_question_id = random.sample((questions_ids - previous_questions_ids), 1)
                returned_question = Question.query.get(selected_question_id).format()
            except:
                returned_question = None

            return jsonify({
                "success": True,
                "question": returned_question,
                "currentCategory": category_id
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
