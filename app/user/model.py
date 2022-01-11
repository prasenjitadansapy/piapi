from datetime import datetime
from app import db, ma
from app.post.model import *
from marshmallow import fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"

class UserSchema(ma.SQLAlchemyAutoSchema):
    # author = ma.Nested(PostSchema, many=True)
    class Meta:
        model = User
        load_instance = True

    author = fields.Nested(PostSchema(), many=True)