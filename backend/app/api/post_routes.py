# backend/app/api/post_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.domain.post import PostCreate, PostDisplay, PostUpdate
from app.use_cases.post_use_cases import PostUseCases
from app.repositories.post_repository import PostRepository
from uuid import uuid4 # --- Import uuid ---

posts_bp = Blueprint('posts', __name__)

post_repo = PostRepository()
post_use_cases = PostUseCases(post_repo)

# --- GET (List) and POST (Create) on the base route ---
@posts_bp.route('/', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        try:
            post_data = PostCreate(**request.json)
            new_post = post_use_cases.create(obj_in=post_data)
            return jsonify(new_post.model_dump()), 201
        except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500
    else: # GET
        posts = post_use_cases.get_all()
        return jsonify([post.model_dump() for post in posts])

# --- GET (Single), PATCH (Update), DELETE (Remove) on the ID route ---
@posts_bp.route('/<uuid:post_id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_post(post_id: uuid4):
    post = post_use_cases.get_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if request.method == 'GET':
        return jsonify(post.model_dump())
    
    elif request.method == 'PATCH':
        try:
            post_update_data = PostUpdate(**request.json)
            updated_post = post_use_cases.update(id=post_id, obj_in=post_update_data)
            return jsonify(updated_post.model_dump())
        except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors()}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500

    elif request.method == 'DELETE':
        post_use_cases.delete_by_id(post_id)
        return '', 204