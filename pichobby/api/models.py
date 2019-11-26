from datetime import datetime as posttime
from pichobby import db, ma
from passlib.hash import pbkdf2_sha256 as phash


class Admin(db.Model):
    """
    Admin backend
    name: name of the administrator
    username: visible name of administrator on the platform
    email: email used by the administrator for messaging
    password: Administrator's passowrd
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String(10), unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = phash.hash(password)

    def verify_password(self, password):
        check = phash.verify(password, self.password)
        return check

    def __repr__(self):
        return '<Admin: {}>'.format(self.username)


class Guest(db.Model):
    """
    Guests
    name: name of the guest
    guestname: visible name of the guest on the platform
    email: email used to contact the guest
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    guestname = db.Column(db.String(8), unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, name, guestname, email):
        self.name = name
        self.guestname = guestname
        self.email = email

    def __repr__(self):
        return '<Guest: {}>'.format(self.guestname)


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


class Comment(db.Model):
    """
    This is the comment section
    comment: comment on the image
    guestname: who commented
    date: date and time of the comment
    pic_id: image to which the comment belongs to
    """

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    guest = db.relationship('Guest', backref=db.backref(
        'guest', lazy='dynamic'
    ))
    guestname = db.Column(db.String, db.ForeignKey('guest.guestname'))
    date = db.Column(db.DateTime)
    pic = db.relationship('Pic', backref=db.backref('pic', lazy='dynamic'))
    pic_id = db.Column(db.String, db.ForeignKey('pic.pic_id'))

    def __init__(self, comment, guestname, pic_id):
        self.comment = comment
        self.guestname = Guest.query.filter_by(guestname=guestname).first()
        self.pic = Pic.query.filter_by(pic_id=pic_id).first()
        self.date = posttime.utcnow()

    def __repr__(self):
        return '<Comment by {}>'.format(self.guestname)


# The Schemas for serialization
class AdminSchema(ma.Schema):
    class Meta:
        fields = ('name', 'username', 'email', 'password')


class GuestSchema(ma.Schema):
    class Meta:
        fields = ('name', 'guestname', 'email')


class PicSchema(ma.Schema):
    class Meta:
        fields = ('pic_id', 'link', 'date', 'likes', 'dislikes')


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('comment', 'guestname', 'date', 'pic_id')
