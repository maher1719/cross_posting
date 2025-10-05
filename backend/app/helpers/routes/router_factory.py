# backend/app/helpers/router_factory.py

from flask import Blueprint, request, jsonify
from pydantic import ValidationError, BaseModel
from typing import Type
from uuid import uuid4

# We'll need our generic use case for type hinting
from app.helpers.crud.crud_use_cases import CRUDUseCases

def create_crud_blueprint(
    *,
    blueprint_name: str,
    use_cases: CRUDUseCases,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    display_schema: Type[BaseModel] = None
) -> Blueprint:
    """
    A factory function that generates a standard RESTful CRUD Blueprint.
    """
    bp = Blueprint(blueprint_name, __name__)

    # --- ROUTE 1 & 2: GET (List All) and POST (Create) ---
    @bp.route('/', methods=['GET', 'POST'])
    def handle_list_and_create():
        if request.method == 'POST':
            try:
                data = create_schema(**request.json)
                new_obj = use_cases.create(obj_in=data)
                return jsonify(new_obj.model_dump()), 201
            except ValidationError as e:
                return jsonify({"error": "Invalid input", "details": e.errors()}), 400
            except Exception as e:
                # Log the full error in a real app
                return jsonify({"error": "An internal server error occurred", "details": e.__str__()}), 500
        else: # GET
            all_objs = use_cases.get_all()
            return jsonify([obj.model_dump() for obj in all_objs])

    # --- ROUTE 3, 4, 5: GET (One), PATCH (Update), DELETE (One) ---
    @bp.route('/<uuid:obj_id>', methods=['GET', 'PATCH', 'DELETE'])
    def handle_single_object(obj_id: uuid4):
        # First, check if the object exists
        obj = use_cases.get_by_id(obj_id)
        if not obj:
            return jsonify({"error": f"{blueprint_name.capitalize()} not found"}), 404

        if request.method == 'GET':
            return jsonify(obj.model_dump())
        
        elif request.method == 'PATCH':
            try:
                update_data = update_schema(**request.json)
                updated_obj = use_cases.update(id=obj_id, obj_in=update_data)
                return jsonify(updated_obj.model_dump())
            except ValidationError as e:
                return jsonify({"error": "Invalid input", "details": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": "An internal server error occurred"+e.__str__()}), 500

        elif request.method == 'DELETE':
            success = use_cases.delete(id=obj_id)
            if success:
                return '', 204
            else: # Should be caught by the initial check, but good for safety
                return jsonify({"error": f"{blueprint_name.capitalize()} not found during deletion"}), 404
    
    return bp