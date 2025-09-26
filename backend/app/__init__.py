# backend/app/__init__.py

from flask import Flask
from config import Config
from .core.db import db, migrate # Use relative import
from .core.celery_utils import make_celery # Use relative import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # We don't need a global celery_app here anymore.
    # The celery instance will be created and attached to the app context.

    # Register blueprints
    from .api.post_routes import posts_bp # Use relative import
    app.register_blueprint(posts_bp, url_prefix='/api/posts')

    from .api.auth_routes import auth_bp # Use relative import
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # This context is still good for ensuring models are found by Flask-Migrate
    with app.app_context():
        from .models import user_model, post_model

    return app

# We need a new way to get the celery instance for our worker.
# We will create a separate entry point for Celery.