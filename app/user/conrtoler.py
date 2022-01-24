from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import json
import logging
import re

from importlib_metadata import email
from app import app, db, bcrypt, jwt
from app.user.model import User

logger = logging.getLogger(__name__)
user = Blueprint('user',__name__, url_prefix='/user')

@user.route("/register", methods = ['POST'])
def register():
    payload = request.json
    check_user_name = User.query.filter_by(username = payload['username']).first()
    check_email = User.query.filter_by(email = payload['email']).first()

    if not re.match(r'[^@]+@[^@]+\.[^@]+', payload['email']):
        resp = Response(json.dumps({'type' : 'error','message' : 'Please Check Email format '}), status=200, mimetype='application/json')
        return resp
    
    if check_email:
        resp = Response(json.dumps({'type' : 'error','message' : 'Email Already Exists'}), status=200, mimetype='application/json')
        return resp
    
    if check_user_name:
        resp = Response(json.dumps({'type' : 'error','message' : 'User Name Already Exists'}), status=200, mimetype='application/json')
        return resp

    if len(payload['username']) <3 or  len(payload['username']) > 31:
        resp = Response(json.dumps({'type' : 'error','message' : 'User Name should be in betwween 3 to 30 character'}), status=200, mimetype='application/json')
        return resp

    if len(payload['password']) <5 or  len(payload['password']) > 31:
        resp = Response(json.dumps({'type' : 'error','message' : 'Password should be in betwween 5 to 30 character'}), status=200, mimetype='application/json')
        return resp

    if payload['password'] != payload['conf_password']:
        resp = Response(json.dumps({'type' : 'error','message' : 'Confirm Password should match with Password'}), status=200, mimetype='application/json')
        return resp
    
    hashed_password = bcrypt.generate_password_hash(payload['password']).decode('utf-8')
    user = User(username = payload['username'], email = payload['email'], password = hashed_password)
    db.session.add(user)
    db.session.commit()
    user_data = {'id' : user.id,'username': user.username, 'email' : user.email}
    resp = Response(json.dumps({'type' : 'Success','message' : 'User created Successfully', 'data' : user_data}), status=201, mimetype='application/json')
    return resp


@user.route("/login", methods = ['POST'])
def login():
    payload = request.json
    user = User.query.filter_by(email = payload['email']).first()
    if user and bcrypt.check_password_hash(user.password, payload['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        reso_data = {'id':user.id, 'username' : user.username, 'email' : user.email}
        resp = Response(json.dumps({'type' : 'Success', 'access_token' : access_token, 'refresh_token' : refresh_token, 'msg' : 'Login Successful', 'data' : reso_data}), status=200, mimetype='application/json')
        return resp
    else:
        resp = Response(json.dumps({'type' : 'Error'}), status=401, mimetype='application/json')
        return resp


@user.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = Response(json.dumps({'type' : 'Success','access_token' : access_token}), status=200, mimetype='application/json')
    return resp
