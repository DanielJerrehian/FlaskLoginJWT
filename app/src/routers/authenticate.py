from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app.src.models.models import User


authenticate = Blueprint("authenticate", __name__)

@authenticate.post("/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter(User.email == email).first()
    if user and user.password == password:
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200
    else: 
        return {"response": "Wrong username or password"}, 401
    
@authenticate.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}
