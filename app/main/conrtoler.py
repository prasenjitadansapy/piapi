from flask import Blueprint, request
import json
from app import post 

main = Blueprint('main',__name__)

@main.route("/", methods = ['GET'])
def hello():
    return json.dumps({'message' : 'Hello world'})
