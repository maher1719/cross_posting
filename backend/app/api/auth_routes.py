# backend/app/api/auth_routes.py

from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from app.domain.user import UserLogin, Token, TokenData, UserDisplay
from app.use_cases.user_use_cases import UserUseCases
from app.repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)

# Initialize dependencies for this blueprint
user_repo = UserRepository()
user_use_cases = UserUseCases(user_repo)


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        user_login_data = UserLogin(**request.json)
        verified_user = user_use_cases.login_user(user_login_data)
        
        if not verified_user:
            return jsonify({"error": "Invalid email or password"}), 401

        # --- THIS IS THE CORRECTED LOGIC ---
        
        # 1. Create the JWT payload and encode the token
        payload = {
            'sub': str(verified_user.id),
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(hours=8)
        }
        secret_key = current_app.config['SECRET_KEY']
        access_token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        # 2. Create the individual Pydantic model instances
        token_obj = Token(access_token=access_token)
        user_display_obj = UserDisplay.from_orm(verified_user)
        
        # 3. Combine them into the parent TokenData object
        token_data_obj = TokenData(token=token_obj, user=user_display_obj)
        
        # 4. Return the complete object
        return jsonify(token_data_obj.model_dump())

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        print(f"--- AN UNEXPECTED ERROR OCCURRED: {e} ---")
        return jsonify({"error": "An internal server error occurred"}), 500