from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import timedelta
import os

app = Flask(__name__)
load_dotenv(dotenv_path=".env")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["ENV"] = "development"
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///models/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)


db = SQLAlchemy(app)
jwt = JWTManager(app)

from app.src.models.models import User

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(User.email == identity).first()

from app.src.routers.index import main
from app.src.routers.authenticate import authenticate

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(authenticate, url_prefix="/auth")