from dotenv import load_dotenv
import os

env_file = ".env.local" if os.getenv("ENV") == "local" else ".env.prod"
load_dotenv(env_file)

from flask import Flask
from flask_cors import CORS
from routes import questions, health
from celery_config import init_celery, app as celery_app



def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(questions.bp)
    app.register_blueprint(health.bp)
    init_celery(app)
     
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=False)
