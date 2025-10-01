# backend/app/api/post_routes.py

from app.helpers.routes.router_factory import create_crud_blueprint
from app.use_cases.post_use_cases import post_use_cases
from app.domain.post import PostCreate, PostUpdate, PostDisplay

# Call the factory to generate the entire blueprint for us!
posts_bp = create_crud_blueprint(
    blueprint_name="posts",
    use_cases=post_use_cases,
    create_schema=PostCreate,
    update_schema=PostUpdate,
    display_schema=PostDisplay
)

# You can still add CUSTOM, non-CRUD routes to this blueprint if needed
# For example:
# @posts_bp.route('/archive-all', methods=['POST'])
# def archive_all_posts():
#     # ... custom logic ...
#     return jsonify({"message": "All posts have been archived."})