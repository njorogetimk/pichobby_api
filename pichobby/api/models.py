from datetime import datetime as posttime
from pichobby import db, ma
from passlib.hash import pbkdf2_sha256 as phash


class User(db.Model):
    """
    User Model; Both the Admin and Guests
    name: name of the user
    username: visible name of the user on the platform
    email: user's contact email
    password: user's password
    level: Boolean; True for admin
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String(10), unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    level = db.Column(db.Boolean)

    def __init__(self, name, username, email, password, level=False):
        self.name = name
        self.username = username
        self.email = email
        self.password = phash.hash(password)
        self.level = level

    def verify_password(self, password):
        check = phash.verify(password, self.password)
        return check

    def __repr__(self):
        return '<User: {}, Level {}>'.format(self.username, self.level)


class Pic(db.Model):
    """
    Image posted on the platform
    pic_id: unique identifier of the image
    link: link to the image
    date: the date and time the image was posted in UTC
    likes: number of likes
    dislikes: number of dislikes
    """

    id = db.Column(db.Integer, primary_key=True)
    pic_id = db.Column(db.String, unique=True)
    link = db.Column(db.String)
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    def __init__(self, pic_id, link):
        self.pic_id = pic_id
        self.link = link
        self.date = posttime.utcnow()
        self.likes = 0
        self.dislikes = 0

    def add_like(self):
        self.likes += 1

    def add_dislike(self):
        self.dislikes += 1

    def __repr__(self):
        return '<Pic {}>'.format(self.pic_id)


class Comment(db.Model):
    """
    This is the comment section
    ctext: comment text on the image
    username: who commented
    date: date and time of the comment
    pic_id: image to which the comment belongs to
    """

    id = db.Column(db.Integer, primary_key=True)
    ctext = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref(
        'user', lazy='dynamic'
    ))
    username = db.Column(db.String, db.ForeignKey('user.username'))
    date = db.Column(db.DateTime)
    pic = db.relationship('Pic', backref=db.backref('pic', lazy='dynamic'))
    pic_id = db.Column(db.String, db.ForeignKey('pic.pic_id'))

    def __init__(self, ctext, username, pic_id):
        self.ctext = ctext
        self.user = User.query.filter_by(username=username).first()
        self.pic = Pic.query.filter_by(pic_id=pic_id).first()
        self.date = posttime.utcnow()

    def __repr__(self):
        return '<Comment by {}>'.format(self.username)


# The Schemas for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'username', 'email', 'email')


class PicSchema(ma.Schema):
    class Meta:
        fields = ('pic_id', 'link', 'date', 'likes', 'dislikes')


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('ctext', 'username', 'date', 'pic_id')
