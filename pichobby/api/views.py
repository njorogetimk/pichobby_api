from flask import jsonify, request
from pichobby.api import picapi
from pichobby.api.models import db
from pichobby.api.models import Pic, User, Comment
from pichobby.api.models import UserSchema, PicSchema, CommentSchema

# Initialize the Schemas
userSchema = UserSchema()
picSchema = PicSchema()
picsSchema = PicSchema(many=True)
commentSchema = CommentSchema()
commentsSchema = CommentSchema(many=True)


@picapi.route('/', methods=['GET'])
def home():
    return jsonify({"Pichobby Api": "My first API"}), 200


@picapi.route('/pics', methods=['GET'])
def get_pics():
    pics = Pic.query.all()
    result = picsSchema.dump(pics)
    return jsonify(result), 200


@picapi.route('/pic/post', methods=['POST'])
def post_pic():
    try:
        pic_id = request.json['pic_id']
        link = request.json['link']
        pic = Pic(pic_id, link)
        db.session.add(pic)
        db.session.commit()
        msg = {"Success": "New pic {} posted".format(pic_id)}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not created"}
        return jsonify(msg), 500


@picapi.route('/pic/<pic_id>', methods=['GET'])
def get_pic(pic_id):
    try:
        pic = Pic.query.filter_by(pic_id=pic_id).first()
        return picSchema.jsonify(pic), 200
    except Exception:
        msg = {"Error": "Not found"}
        return jsonify(msg), 404


@picapi.route('/add/user', methods=['POST'])
def add_user():
    try:
        name = request.json['name']
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        user = User(name, username, email, password)
        db.session.add(user)
        db.session.commit()
        msg = {"Success": "User {} added".format(username)}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not created"}
        return jsonify(msg), 500


@picapi.route('/user/<username>', methods=['GET'])
def get_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        return userSchema.jsonify(user), 200
    except Exception:
        msg = {"Error": "Not found"}
        return jsonify(msg), 404


@picapi.route('/post/comment', methods=['POST'])
def post_comment():
    try:
        ctext = request.json['ctext']
        username = request.json['username']
        pic_id = request.json['pic_id']
        pic = Pic.query.filter_by(pic_id=pic_id).first()
        if not pic:
            return jsonify({"Error": "Invalid pic_id"}), 403
        comment = Comment(ctext, username, pic_id)
        db.session.add(comment)
        db.session.commit()
        msg = {"Success": "Comment posted"}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not posted"}
        return jsonify(msg), 500


@picapi.route('/pic/<pic_id>/comments', methods=['GET'])
def get_pic_comments(pic_id):
    try:
        comments = Comment.query.filter_by(pic_id=pic_id).all()
        results = commentsSchema.dump(comments)
        return jsonify({pic_id: results}), 200
    except Exception:
        msg = {"Error": "No Comment"}
        return jsonify(msg), 404


@picapi.route('/pic/<pic_id>/like', methods=['POST'])
def add_like(pic_id):
    try:
        pic = Pic.query.filter_by(pic_id=pic_id).first()
        pic.add_like()
        msg = {"Success": "Like added"}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Failed"}
        return jsonify(msg), 500


@picapi.route('/pic/<pic_id>/dislike', methods=['POST'])
def add_dislike(pic_id):
    try:
        pic = Pic.query.filter_by(pic_id=pic_id).first()
        pic.add_dislike()
        msg = {"Success": "Dislike added"}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Failed"}
        return jsonify(msg), 500
