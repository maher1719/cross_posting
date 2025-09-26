# backend/celery_worker.py

from app import create_app
from app.core.celery_utils import make_celery

flask_app = create_app()
celery = make_celery(flask_app)