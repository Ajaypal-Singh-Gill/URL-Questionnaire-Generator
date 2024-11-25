from flask import Blueprint, request, jsonify, make_response
from services.question_service import process_question_generation
from db.dbconfig import get_db
import logging
import os

bp = Blueprint('questions', __name__)
logging.basicConfig(level=logging.DEBUG)

@bp.route('/generate-question', methods=['POST', 'OPTIONS'])
def generate_question():
    frontend_url = os.getenv('FE_URL', 'http://localhost:3000')
    print("FE_URL:", frontend_url)

    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers["Access-Control-Allow-Origin"] = frontend_url
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    data = request.get_json()
    url = data.get('url')
    save_to_db = data.get('save_to_db', True)

    if not url:
        return jsonify({'error': 'Invalid URL'}), 400

    db = next(get_db())
    result = process_question_generation(db, url, save_to_db)
    
    return jsonify(result)
