from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
# from flask_marshmallow import Marshmallow

app = Flask(__name__)
cors = CORS(app)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
# ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

##Modules Import
from app.user.conrtoler import user
from app.post.conrtoler import post
from app.main.conrtoler import main

## Create Blueprint of Modules
app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(main)

