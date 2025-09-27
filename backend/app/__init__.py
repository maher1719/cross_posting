# backend/app/__init__.py

from flask import Flask
from config import Config
from flask_cors import CORS
from .core.db import db, migrate
from .core.celery_utils import celery_app, make_celery

def create_app(config_class=Config):
    """
    The application factory. This function builds the Flask app object.
    """
    app = Flask(__name__)
    
    # 1. Load configuration from the 'config.py' file and .env variables
    app.config.from_object(config_class)
    CORS(app) 
    # 2. Initialize Flask extensions
    # These objects are created in /core but are "bound" to our app here.
    db.init_app(app)
    migrate.init_app(app, db)
    
    # The Celery instance is not created here directly, but the factory
    # to create it is available for our celery_worker.py entrypoint.
    make_celery(app)
    # 3. Register Blueprints
    # This is how we connect our modular route files to the main app.
    from .api.post_routes import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/api/posts')

    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .api.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # 4. Ensure models are discovered by Flask-Migrate
    # This 'with' block ensures that when we run 'flask db migrate',
    # SQLAlchemy knows about all the classes defined in our model files.
    with app.app_context():
        from .models import user_model, post_model

    return app