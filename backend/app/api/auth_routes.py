# backend/app/api/auth_routes.py

from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "User login endpoint."})