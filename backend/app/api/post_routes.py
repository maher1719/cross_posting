# backend/app/api/post_routes.py

from flask import Blueprint, jsonify, request
import traceback
from pydantic import ValidationError
from app.domain.post import PostCreate, PostDisplay, PostUpdate
from app.use_cases.post_use_cases import PostUseCases
from app.repositories.post_repository import PostRepository

posts_bp = Blueprint('posts', __name__)

post_repo = PostRepository()
post_use_cases = PostUseCases(post_repo)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    try:
        posts = post_use_cases.get_all_posts()
        # --- ENHANCEMENT: Use modern Pydantic V2 .model_dump() ---
        return jsonify([post.model_dump() for post in posts])
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500

@posts_bp.route('/', methods=['POST'])
def create_post():
    try:
        post_data = PostCreate(**request.json)
        new_post = post_use_cases.create_post(post_data)
        return jsonify(new_post.model_dump()), 201
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = post_use_cases.get_by_id(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        return jsonify(post.model_dump())
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post_by_id(post_id):
    try:
        success = post_use_cases.delete_by_id(post_id)
        if not success:
            return jsonify({"error": "Post not found"}), 404
        # --- ENHANCEMENT: Standard is to return 204 No Content on successful delete ---
        return '', 204
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500

@posts_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_posts_by_user_id(user_id):
    try:
        num_deleted = post_use_cases.delete_by_user_id(user_id)
        return jsonify({"message": f"{num_deleted} posts deleted successfully"}), 200
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500

@posts_bp.route('/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    # --- ENHANCEMENT: Use PATCH for partial updates and get ID from URL for RESTful consistency ---
    try:
        # Combine URL parameter with request body
        post_data = PostUpdate(id=post_id, **request.json)
        updated_post = post_use_cases.update(post_data)
        if not updated_post:
            return jsonify({"error": "Post not found"}), 404
        return jsonify(updated_post.model_dump()), 200
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500