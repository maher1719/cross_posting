# backend/app/api/post_routes.py

from flask import Blueprint, jsonify

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    return jsonify({"message": "This will return posts."})