from flask import Blueprint, request, jsonify
import json
from app import db
from app.post.model import *

post = Blueprint('post',__name__)

post_list = []

@post.route("/post/new-post", methods = ['POST'])
def newPost():
    data = request.json
    post_list.append(data)
    return json.dumps(data)


@post.route("/post/<int:post_id>/view", methods = ['POST'])
def viewPost(post_id):
    print(post_id)
    return json.dumps({'message' : 'view Post'})


@post.route("/post/<int:post_id>/update", methods = ['POST'])
def updatePost(post_id):
    print(post_id)
    return json.dumps({'message' : 'Update Post'})


@post.route("/post/<int:post_id>/delete", methods = ['POST'])
def deletePost(post_id):
    print(post_id)
    return json.dumps({'message' : 'Delete Post'})


@post.route("/post/all-posts", methods = ['POST'])
def allPosts():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    post_data = post_schema.dump(posts)
    
    return json.dumps({"data": post_data})
