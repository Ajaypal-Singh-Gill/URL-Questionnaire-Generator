from flask import Flask
from flask_cors import CORS
from routes import questions, health

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(questions.bp)
    app.register_blueprint(health.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5001, debug=False)
