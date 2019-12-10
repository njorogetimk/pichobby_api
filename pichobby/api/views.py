from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_claims, verify_jwt_in_request,
)
from functools import wraps
from pichobby import jwt
from pichobby.api import picapi
from pichobby.api.models import (
    db, Pic, Users, Comment, PicLikes, UserSchema, PicSchema, CommentSchema,
    PicLikeSchema
)
import os
import markdown

# Initialize the Schemas
userSchema = UserSchema()
usersSchema = UserSchema(many=True)
picSchema = PicSchema()
picsSchema = PicSchema(many=True)
commentSchema = CommentSchema()
commentsSchema = CommentSchema(many=True)
picLikeSchema = PicLikeSchema()
picLikesSchema = PicLikeSchema(many=True)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = Users.query.filter_by(username=identity).first()
    if user.level:
        return {'roles': 'admin'}
    else:
        return {'roles': 'guest'}


@picapi.route('/', methods=['GET'])
def home():
    filePath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    mdFile = filePath+'/README.md'
    with open(mdFile) as markdown_file:
        content = markdown_file.read()
    documentation = markdown.markdown(content)
    return jsonify({"Pichobby Api": documentation}), 200


@picapi.route('/login', methods=['GET'])
def login():
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            print(not auth)
            return jsonify({"msg": "Invalid Login"}), 401
        username = auth.username
        password = auth.password
        user = Users.query.filter_by(username=username).first()
        if not username or not user or not password:
            return jsonify({"Message": "Invalid login parameters"}), 400
        passcheck = user.verify_password(password)
        if not passcheck:
            return jsonify({"Message": "Invalid login parameters"}), 400

        access_token = create_access_token(identity=username)
        return jsonify(access_token), 200
    except Exception:
        return jsonify({"Message": "Failed Login"}), 400


@picapi.route('/add/user', methods=['POST'])
@jwt_required
@admin_required
def add_user():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        name = request.json.get('name', None)
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not name or not username or not email or not password:
            return jsonify({"Msg": "Missing JSON info"}), 400
        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({"Msg": "User already present"}), 200
        user = Users(name, username, email, password)
        db.session.add(user)
        db.session.commit()
        msg = {"Success": "User {} added".format(username)}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not created"}
        return jsonify(msg), 500


@picapi.route('/guests', methods=['GET'])
def get_users():
    users = Users.query.filter_by(level=False).all()
    result = usersSchema.dump(users)
    return jsonify({"Users Present": result}), 200


@picapi.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"Error": "{} not found".format(username)}), 404
    return userSchema.jsonify(user), 200


@picapi.route('/pic/post', methods=['POST'])
@jwt_required
def post_pic():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        pic_id = request.json.get('pic_id', None)
        link = request.json.get('link', None)
        if not pic_id or not link:
            return jsonify({"msg": "Missing JSON info"}), 400
        pic = Pic(pic_id, link)
        db.session.add(pic)
        db.session.commit()
        msg = {"Success": "New pic {} posted".format(pic_id)}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not created"}
        return jsonify(msg), 500


@picapi.route('/pics', methods=['GET'])
def get_pics():
    pics = Pic.query.all()
    result = picsSchema.dump(pics)
    return jsonify({"Posted Pictures": result}), 200


@picapi.route('/pic/<pic_id>', methods=['GET'])
def get_pic(pic_id):
    pic = Pic.query.filter_by(pic_id=pic_id).first()
    if not pic:
        return jsonify({"Error": "{} not found".format(pic_id)}), 404
    return picSchema.jsonify(pic), 200


@picapi.route('/post/comment', methods=['POST'])
@jwt_required
def post_comment():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        ctext = request.json.get('ctext', None)
        username = request.json.get('username', None)
        pic_id = request.json.get('pic_id', None)
        if not ctext or not username or not pic_id:
            return jsonify({"msg": "Missing JSON info"}), 400
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
    pic = Pic.query.filter_by(pic_id=pic_id).first()
    if not pic:
        return jsonify({"Error": pic_id+" not found"}), 404
    comments = Comment.query.filter_by(pic_id=pic_id).all()
    results = commentsSchema.dump(comments)
    return jsonify({pic_id+" comments": results}), 200


@picapi.route('/pic/<pic_id>/like', methods=['POST'])
@jwt_required
def add_like(pic_id):
    try:
        pic = Pic.query.filter_by(pic_id=pic_id).first()
        if not pic:
            return jsonify({"msg": pic_id+" not found"}), 404
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        like = request.json.get('like', None)
        username = request.json.get('username', None)
        if like is None or not username:
            return jsonify({"msg": "Missing JSON info"}), 400
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"Error": "User not found"}), 404
        likeCheck = PicLikes.query.filter_by(username=username).filter_by(
            pic_id=pic_id
        ).first()
        if likeCheck:
            return jsonify({"Error": "Like already added"}), 200
        picLike = PicLikes(like, username, pic_id)
        db.session.add(picLike)
        db.session.commit()
        msg = {"Success": "Like added"}
        return jsonify(msg), 201
    except Exception as e:
        print(e)
        msg = {"Error": "Failed"}
        return jsonify(msg), 500


@picapi.route('/pic/<pic_id>/likes', methods=['GET'])
def get_pic_likes(pic_id):
    try:
        piccheck = Pic.query.filter_by(pic_id=pic_id).first()
        if not piccheck:
            return jsonify({"Error": pic_id+" not found"}), 404
        picLikes = PicLikes.query.filter_by(pic_id=pic_id).all()
        results = picLikesSchema.dump(picLikes)
        return jsonify({"{} likes and dislikes".format(pic_id): results})
    except Exception:
        return jsonify({"Error": "Failed to retrieve likes"}), 500


@picapi.route('/<username>/mylikes', methods=['GET'])
def get_mylikes(username):
    try:
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({'Error': "User not found"}), 404
        piclikes = PicLikes.query.filter_by(username=username).all()
        results = picLikesSchema.dump(piclikes)
        return jsonify({"My Likes": results}), 200
    except Exception:
        return jsonify({"Error": "Failed to retrieve likes"}), 500
