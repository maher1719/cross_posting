# backend/celery_worker.py

from app import create_app
from app.core.celery_utils import celery_app

flask_app = create_app()
celery = celery_app