# backend/app/api/user_routes.py

from flask import Blueprint, request, jsonify
from pydantic import ValidationError



from app.domain.user import UserCreate
from app.use_cases.user_use_cases import UserUseCases
from app.repositories.user_repository import UserRepository

# Define the blueprint
user_bp = Blueprint('users', __name__)

# Initialize dependencies
user_repo = UserRepository()
user_use_cases = UserUseCases(user_repo)

# --- THE FIX IS ON THIS LINE ---
@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        # 1. Get raw JSON and validate with Pydantic
        user_data = UserCreate(**request.json)
        
        # 2. Call the Use Case layer with validated data
        new_user = user_use_cases.register_new_user(user_data)
        
        # 3. Return a successful HTTP response
        return jsonify(new_user.dict()), 201 # 201 Created

    except ValidationError as e:
    # Pydantic's e.errors() method gives a clean, structured list of errors
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except ValueError as e:
        # Handle business logic errors (e.g., email exists)
        return jsonify({"error": str(e)}), 409 # 409 Conflict
    except Exception as e:
        # --- ADD THESE TWO LINES FOR DEBUGGING ---
        print("--- AN UNEXPECTED ERROR OCCURRED ---")
        #traceback.print_exc()
        # -----------------------------------------
        
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred"+e.__str__()}), 500