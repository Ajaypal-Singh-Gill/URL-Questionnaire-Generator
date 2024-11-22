from celery import Celery
import os
from dotenv import load_dotenv

env_file = ".env.local" if os.getenv("ENV") == "local" else ".env.prod"
load_dotenv(env_file)
print("CELERY_REDIS_BROKER_URL:", os.getenv('CELERY_REDIS_BROKER_URL'))
print("CELERY_REDIS_BACKEND_URL:", os.getenv('CELERY_REDIS_BACKEND_URL'))

app = Celery('backend', broker=os.getenv('CELERY_REDIS_BROKER_URL'), backend=os.getenv('CELERY_REDIS_BACKEND_URL'))
# app.conf.update(
#     broker_use_ssl={
#         'ssl_cert_reqs': 'CERT_NONE'
#     },
#     result_backend_use_ssl={
#         'ssl_cert_reqs': 'CERT_NONE'
#     }
# )

def init_celery(flask_app):
    app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )

    class FlaskTask(app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    app.Task = FlaskTask

app.autodiscover_tasks(['services'])
