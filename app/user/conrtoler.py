from flask import Blueprint, request
import json

user = Blueprint('user',__name__)

@user.route("/register", methods = ['GET', 'POST'])
def register():
    data = json.dumps({'hello' : 'world'})
    return data