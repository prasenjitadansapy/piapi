from flask import Blueprint, request, jsonify, Response
import json
from app import app, db
from app.post.model import Post
from app.utilities.util import AlchemyEncoder
from app.utilities.handle_error import handle_error
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity

logger = logging.getLogger(__name__)
post = Blueprint('post',__name__, url_prefix='/post')

post_list = []

@post.route("/new-post", methods = ['POST'])
@jwt_required()
def newPost():
    try:
        payload = request.json
        payload['user_id'] = get_jwt_identity()
        crt_post = Post(**payload)
        db.session.add(crt_post)
        db.session.commit()
        resp = Response(json.dumps({'type':'success','msg': 'Post Successfull', 'id': crt_post.id}), status=201, mimetype='application/json')
        return resp    
    except Exception as e:
        db.session.delete(crt_post)
        db.session.commit()
        return handle_error(e, logger)


@post.route("/<int:post_id>/view", methods = ['POST'])
@jwt_required()
def viewPost(post_id):
    try:
        itr = Post.query.filter_by(id = post_id).first()
        if itr:
            data = json.dumps(itr, cls=AlchemyEncoder)
            payload_data = json.loads(data)
            for i in ['author','registry']:
                payload_data.pop(i)

            resp = Response(json.dumps(payload_data), status=200, mimetype='application/json')
            return resp
        else:
            resp = Response(json.dumps({'type' : 'error','message' : 'Post Not Found'}), status=200, mimetype='application/json')
            return resp
    except Exception as e:
        return handle_error(e, logger)


@post.route("/update", methods = ['POST'])
def updatePost():
    try:
        data = request.json
        itr = Post.query.filter_by(id = data['id']).first()
        if itr:
            post = Post(**data)
            db.session.merge(post)
            db.session.commit()
            resp = Response(json.dumps({'type' : 'success','message' : 'Update Post'}), status=200, mimetype='application/json')
            return resp
        else:
            resp = Response(json.dumps({'type' : 'error','message' : 'Post Not Found'}), status=200, mimetype='application/json')

    except Exception as e:
        return handle_error(e, logger)

@post.route("/<int:post_id>/delete", methods = ['POST'])
def deletePost(post_id):
    try:
        delete_post = Post.query.get(post_id)
        if delete_post:
            db.session.delete(delete_post)
            db.session.commit()
            resp = Response(json.dumps({'type' : 'success','message' : 'Post Deleted', 'id' : delete_post.id}), status=200, mimetype='application/json')
            return resp
        else:
            resp = Response(json.dumps({'type' : 'Error','message' : 'Post not found', 'id' : post_id}), status=200, mimetype='application/json')
            return resp

    except Exception as e:
        return handle_error(e, logger)


@post.route("/all-posts", methods = ['POST'])
def allPosts():
    try:
        itr = Post.query.all()
        if itr:
            posts = json.dumps(itr, cls=AlchemyEncoder)
            #print(posts)
            
            resp = Response(posts, status=200, mimetype='application/json')
            return resp
        else:
            resp = Response(json.dumps({'type' : 'Error','message' : 'Post not found'}), status=200, mimetype='application/json')
            return resp
    except Exception as e:
        return handle_error(e, logger)


