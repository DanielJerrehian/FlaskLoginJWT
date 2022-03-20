from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user


main = Blueprint("index", __name__)

@main.get("/")
@jwt_required(optional=True)
def index():
    return f"Hey {current_user.username}!" if current_user else "Hey!"

@main.get("/public")
def public():
    return "Anyone can view this route"

@main.get("/private")
@jwt_required()
def private():
    return jsonify(f"Hey {current_user.username}, your email is {current_user.email}!"), 200


    