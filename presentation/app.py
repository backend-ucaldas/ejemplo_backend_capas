# presentation/app.py
from flask import Flask, request, jsonify
from business.user_service import UserService

app = Flask(__name__)

# --- User endpoints ---

@app.route("/users", methods=["GET"])
def get_users():
    users = UserService.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    try:
        user = UserService.create_user(data.get("name"), data.get("email"))
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return jsonify(user.to_dict()), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    try:
        user = UserService.update_user(user_id, data.get("name"), data.get("email"))
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# --- Post endpoints ---

@app.route("/users/<int:user_id>/posts", methods=["POST"])
def add_post(user_id):
    data = request.get_json()
    if not data.get("title") or not data.get("content"):
        return jsonify({"message": "Title and content are required"}), 400
    post = UserService.add_post(user_id, data["title"], data["content"])
    if post:
        return jsonify(post.to_dict()), 201
    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
