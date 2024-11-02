from flask import Blueprint

bp = Blueprint('health', __name__)

@bp.route('/ping', methods=['GET'])
def ping():
    return "Pong"
