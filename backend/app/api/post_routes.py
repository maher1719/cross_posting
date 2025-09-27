# backend/app/api/post_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.domain.post import PostCreate
from app.use_cases.post_use_cases import PostUseCases
from app.repositories.post_repository import PostRepository


posts_bp = Blueprint('posts', __name__) # what is this __name__?


post_repo = PostRepository()
post_use_cases = PostUseCases(post_repo)




@posts_bp.route('/', methods=['GET'])
def get_posts():
    try:
        posts = post_use_cases.get_all_posts()
        return jsonify([post.dict() for post in posts])
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500




@posts_bp.route('/', methods=['POST'])
def create_post():
    try:
        post_data = PostCreate(**request.json)
        new_post = post_use_cases.create_post(post_data)
        return jsonify(new_post.dict()), 201
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500



@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = post_use_cases.get_by_id(post_id)
        print(post.dict())
        if post:
            return jsonify(post.dict())
        else:
            return jsonify({"error": "Post not found"}), 404
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500



@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = post_use_cases.delete_by_id(post_id)
        if post:
            return jsonify({"message": "Post deleted successfully"}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500




@posts_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_posts_by_user_id(user_id):
    try:
        post = post_use_cases.delete_by_user_id(user_id)
        if post:
            return jsonify({"message": "Posts deleted successfully"}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500



@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id, content):
    try:
        post = post_use_cases.update(post_id, content)
        if post:
            return jsonify(post.dict()), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500

        