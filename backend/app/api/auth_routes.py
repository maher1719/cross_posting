# backend/app/api/auth_routes.py

from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from app.domain.user import UserLogin, Token
from app.use_cases.user_use_cases import UserUseCases
from app.repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)

# Initialize dependencies for this blueprint
user_repo = UserRepository()
user_use_cases = UserUseCases(user_repo)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # 1. Validate incoming JSON against the Pydantic model
        user_login_data = UserLogin(**request.json)
        
        # 2. Call the use case to handle all business logic
        verified_user = user_use_cases.login_user(user_login_data)
        
        # 3. Handle authentication failure
        if not verified_user:
            return jsonify({"error": "Invalid email or password"}), 401

        # 4. If authentication is successful, create the JWT
        payload = {
            'sub': str(verified_user.id),  # The "subject" of the token is the user's ID
            'iat': datetime.now(timezone.utc), # "Issued At" timestamp
            'exp': datetime.now(timezone.utc) + timedelta(hours=8) # Expiration timestamp
        }
        
        secret_key = current_app.config['SECRET_KEY']
        access_token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        # 5. Return the token to the client
        return jsonify(Token(access_token=access_token).model_dump())

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        # In a real app, you would log the full error here
        print(e)
        return jsonify({"error": "An internal server error occurred "+e.__str__()}), 500