from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from app.config import Config, JWT_SUPER_SECRET_KEY
from flask_jwt_extended import JWTManager
from datetime import timedelta
# from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# ma = Marshmallow(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
app.config["JWT_SECRET_KEY"] = JWT_SUPER_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

##Modules Import
from app.user.conrtoler import user
from app.post.conrtoler import post
from app.main.conrtoler import main

## Create Blueprint of Modules
app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(main)

