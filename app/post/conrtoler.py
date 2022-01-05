from flask import Blueprint, request
import json

from app import post 

post = Blueprint('post',__name__)