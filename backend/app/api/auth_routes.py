# backend/app/api/auth_routes.py


from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.domain.user import UserLogin
from app.use_cases.user_use_cases import UserUseCases
from app.repositories.user_repository import UserRepository


auth_bp = Blueprint('auth', __name__)


# Initialize dependencies
user_repo = UserRepository()
user_use_cases = UserUseCases(user_repo)



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
            # 1. Get raw JSON and validate with Pydantic
            user_login_data = UserLogin(**request.json)
            #print(request.json)
            
            # 2. Call the Use Case layer with validated data
            verified_user = user_use_cases.verify_login_user(user_login_data)
            #print(verified_user)
            # 3. Return a successful HTTP response
            if(verified_user):
                return jsonify(verified_user.dict()), 201 # 201 Created
            return {"error": "Invalid email or password"}
    except ValidationError as e:
        # Handle Pydantic validation errors
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
        return jsonify({"error": "An unexpected error occurred"+str(e)}), 500