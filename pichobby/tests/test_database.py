import unittest
from pichobby import create_app, db
from pichobby.api.models import User, Pic, Comment, PicLikes


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_User(self):
        admin = User('tim', 'tim', 'm@r.co', '123', True)
        guest = User('njosh', 'njosh', 'r@g.com', '345')
        db.session.add(admin)
        db.session.add(guest)
        try:
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            success = False
            msg = e
        self.assertTrue(success, msg)

    def test_Pic(self):
        pic = Pic('sunset1', 'tohere')
        db.session.add(pic)
        try:
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            success = False
            msg = e
        self.assertTrue(success, msg)

    def test_Comment(self):
        username = 'kin'
        pic_id = 'sunset1'
        kin = User('kin', username, 'k@e', '123')
        pic = Pic(pic_id, 'tohere')
        comment = Comment('here', username, pic_id)
        db.session.add(kin)
        db.session.add(pic)
        try:
            db.session.commit()
            db.session.add(comment)
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            msg = e
            success = False
        self.assertTrue(success, msg)

    def test_Like(self):
        username = 'kin'
        pic_id = 'sunset1'
        kin = User('kin', username, 'k@e', '123')
        pic = Pic(pic_id, 'tohere')
        db.session.add(kin)
        db.session.add(pic)

        try:
            db.session.commit()
            like = PicLikes(True, username, pic_id)
            db.session.add(like)
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            msg = e
            success = False

        self.assertTrue(success, msg)


if __name__ == '__main__':
    unittest.main()
