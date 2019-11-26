import unittest
from pichobby import create_app, db
from pichobby.api.models import Admin, Guest, Pic, Comment


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

    def test_Admin(self):
        tim = Admin('tim', 'njosh', 'm@r.co', '123')
        db.session.add(tim)
        try:
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            success = False
            msg = e
        self.assertTrue(success, msg)

    def test_Guest(self):
        kin = Guest('kin', 'kin', 'k@e')
        usernameDup = Guest('ki', 'kin', 'ke@e')
        emailDup = Guest('ki', 'kino', 'k@e')
        db.session.add(kin)
        try:
            db.session.commit()
            success = True
            msg = ''
        except Exception as e:
            success = False
            msg = e
        self.assertTrue(success, msg)

        db.session.add(usernameDup)
        try:
            # Has created a username duplicate
            db.session.commit()
            noDuplicate = False
        except Exception:
            # Has not created a username duplicate
            noDuplicate = True
        self.assertTrue(noDuplicate, msg="Has created a usename duplicate")

        db.session.add(emailDup)
        try:
            # Has created an email duplicate
            db.session.commit()
            noDuplicate = False
        except Exception:
            # Has not created an email duplicate
            noDuplicate = True
        self.assertTrue(noDuplicate, msg="Has created an email duplicate")

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

        # Tesitng likes and dislikes
        mypic = Pic.query.filter_by(pic_id='sunset1').first()
        mypic.add_like()
        mypic.add_dislike()
        self.assertTrue(mypic.likes > 0)
        self.assertTrue(mypic.dislikes > 0)

    def test_Comment(self):
        guestname = 'kin'
        pic_id = 'sunset1'
        kin = Guest('kin', guestname, 'k@e')
        pic = Pic(pic_id, 'tohere')
        comment = Comment('here', guestname, pic_id)
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


if __name__ == '__main__':
    unittest.main()
