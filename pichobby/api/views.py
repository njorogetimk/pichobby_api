from flask import jsonify, request
from pichobby.api import picapi
from pichobby.api.models import db
from pichobby.api.models import Pic, Guest, Comment
from pichobby.api.models import AdminSchema, GuestSchema, PicSchema
from pichobby.api.models import CommentSchema

# Initialize the Schemas
adminSchema = AdminSchema()
guestSchema = GuestSchema()
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


@picapi.route('/add/guest', methods=['POST'])
def add_guest():
    try:
        name = request.json['name']
        guestname = request.json['guestname']
        email = request.json['email']
        guest = Guest(name, guestname, email)
        db.session.add(guest)
        db.session.commit()
        msg = {"Success": "Guest {} added".format(guestname)}
        return jsonify(msg), 201
    except Exception:
        msg = {"Error": "Not created"}
        return jsonify(msg), 500


@picapi.route('/guest/<guestname>', methods=['GET'])
def get_guest(guestname):
    try:
        guest = Guest.query.filter_by(guestname=guestname).first()
        return guestSchema.jsonify(guest), 200
    except Exception:
        msg = {"Error": "Not found"}
        return jsonify(msg), 404


@picapi.route('/post/comment', methods=['POST'])
def post_comment():
    try:
        ctext = request.json['ctext']
        guestname = request.json['guestname']
        pic_id = request.json['pic_id']
        comment = Comment(ctext, guestname, pic_id)
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
        results = commentSchema.dump(comments)
        return jsonify(results), 200
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
