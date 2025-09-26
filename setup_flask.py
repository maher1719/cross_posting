# setup_flask.py
import os
import textwrap

# --- Configuration ---
BACKEND_DIR = "backend"
APP_DIR = os.path.join(BACKEND_DIR, "app")

# Dictionary of directories and their subdirectories/files
DIRS = {
    BACKEND_DIR: {
        "app": {
            "api": ["__init__.py", "post_routes.py", "auth_routes.py"],
            "services": ["__init__.py", "posting_service.py", "image_service.py"],
            "models": ["__init__.py", "user_model.py", "post_model.py"],
            "core": ["__init__.py", "db.py", "celery_utils.py"],
            "__init__.py": None,
        },
        "migrations": [],
        "tests": ["__init__.py"],
        ".flaskenv": None,
        "config.py": None,
        "run.py": None,
        "requirements.txt": None,
    }
}

# Dictionary of file contents
FILE_CONTENTS = {
    "run.py": textwrap.dedent("""\
        from app import create_app, celery_app

        app = create_app()

        if __name__ == "__main__":
            app.run()
    """),
    
    "config.py": textwrap.dedent("""\
        import os
        from dotenv import load_dotenv

        load_dotenv()

        class Config:
            SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
            CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    """),
    
    os.path.join("app", "__init__.py"): textwrap.dedent("""\
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate
        from config import Config
        from app.core.db import db, migrate
        from app.core.celery_utils import make_celery

        celery_app = None

        def create_app(config_class=Config):
            app = Flask(__name__)
            app.config.from_object(config_class)

            # Initialize extensions
            db.init_app(app)
            migrate.init_app(app, db)

            # Update celery config
            global celery_app
            celery_app = make_celery(app)
            
            # Register blueprints
            from app.api.post_routes import posts_bp
            app.register_blueprint(posts_bp, url_prefix='/api/posts')

            from app.api.auth_routes import auth_bp
            app.register_blueprint(auth_bp, url_prefix='/api/auth')
            
            with app.app_context():
                # Import models here to ensure they are registered with SQLAlchemy
                from app.models import user_model, post_model

            return app
    """),

    os.path.join("app", "core", "db.py"): textwrap.dedent("""\
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate

        db = SQLAlchemy()
        migrate = Migrate()
    """),
    
    os.path.join("app", "core", "celery_utils.py"): textwrap.dedent("""\
        from celery import Celery

        def make_celery(app):
            celery = Celery(
                app.import_name,
                backend=app.config['CELERY_RESULT_BACKEND'],
                broker=app.config['CELERY_BROKER_URL']
            )
            celery.conf.update(app.config)

            class ContextTask(celery.Task):
                def __call__(self, *args, **kwargs):
                    with app.app_context():
                        return self.run(*args, **kwargs)

            celery.Task = ContextTask
            return celery
    """),

    os.path.join("app", "api", "post_routes.py"): textwrap.dedent("""\
        from flask import Blueprint, jsonify

        posts_bp = Blueprint('posts', __name__)

        @posts_bp.route('/', methods=['GET'])
        def get_posts():
            return jsonify({"message": "This will return posts."})
    """),

    os.path.join("app", "api", "auth_routes.py"): textwrap.dedent("""\
        from flask import Blueprint, jsonify

        auth_bp = Blueprint('auth', __name__)

        @auth_bp.route('/login', methods=['POST'])
        def login():
            return jsonify({"message": "User login endpoint."})
    """),

    os.path.join("app", "models", "user_model.py"): textwrap.dedent("""\
        from app.core.db import db
        import datetime

        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

            def __repr__(self):
                return f'<User {self.username}>'
    """),
    
    ".flaskenv": textwrap.dedent("""\
        FLASK_APP=run.py
        FLASK_DEBUG=1
    """),
    
    "requirements.txt": textwrap.dedent("""\
        Flask
        Flask-SQLAlchemy
        Flask-Migrate
        psycopg2-binary
        python-dotenv
        Pillow
        celery
        redis
        gunicorn
    """),
}

def create_structure(base_path, structure):
    """Recursively creates directories and files."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # It's a directory with content
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            # It's a directory with a list of files/subdirs
            os.makedirs(path, exist_ok=True)
            for item in content:
                create_structure(path, {item: None})
        else:
            # It's a file
            if path not in created_files:
                print(f"Creating file: {path}")
                # Get content from the dictionary if it exists
                # We use a relative path for the key
                relative_path = os.path.relpath(path, start=BACKEND_DIR) if base_path.startswith(BACKEND_DIR) else name
                content_to_write = FILE_CONTENTS.get(relative_path, "")
                with open(path, 'w') as f:
                    f.write(content_to_write)
                created_files.add(path)

if __name__ == "__main__":
    print("--- Setting up Flask Clean Architecture ---")
    created_files = set()
    create_structure(os.getcwd(), DIRS)
    print("\n--- Setup Complete! ---")
    print(f"Flask project created in '{BACKEND_DIR}' directory.")
    print("\nNext steps:")
    print("1. Set up your .env file with database and secret keys.")
    print("2. Run 'pip install -r backend/requirements.txt' to install dependencies.")
    print("3. Initialize the database with 'flask db init', 'flask db migrate', 'flask db upgrade'.")