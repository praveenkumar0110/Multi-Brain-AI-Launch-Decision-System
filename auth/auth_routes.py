from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

users = {}  # demo (MongoDB later)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    users[data["email"]] = data["password"]
    return jsonify(msg="Registered successfully")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if users.get(data["email"]) == data["password"]:
        token = create_access_token(identity=data["email"])
        return jsonify(access_token=token)
    return jsonify(msg="Invalid login"), 401
