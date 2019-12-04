import unittest
from pichobby import create_app, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home(self):
        rt = self.client.get('/')
        self.assertEqual(rt.status_code, 200)

    def test_pics(self):
        rt = self.client.get('/pics')
        self.assertEqual(rt.status_code, 200)

    def test_pic_post(self):
        pic = {
            "pic_id": "myid", "link": "/to/no/where"
        }
        rt = self.client.post('/pic/post', json=pic)
        self.assertEqual(rt.status_code, 201)
        nopic = {"pic_id": "myid", "link": "/to/no/where"}
        rt = self.client.post('/pic/post', json=nopic)
        self.assertEqual(rt.status_code, 500)

    def test_pic_get(self):
        pic = {
            "pic_id": "myid", "link": "/to/no/where"
        }
        rt = self.client.post('/pic/post', json=pic)
        self.assertEqual(rt.status_code, 201)
        rt = self.client.get('pic/myid')
        self.assertEqual(rt.status_code, 200)

    def test_user_add(self):
        user = {
            "name": "mgeni", "username": "mgeni", "email": "r@e",
            "password": "123"
        }
        rt = self.client.post('/add/user', json=user)
        self.assertEqual(rt.status_code, 201)

    def test_user_get(self):
        self.test_user_add()
        rt = self.client.get('/user/mgeni')
        self.assertEqual(rt.status_code, 200)

    def test_comment_post(self):
        user = {
            "name": "mgeni", "username": "mgeni", "email": "r@e",
            "password": "123"
        }
        rt1 = self.client.post('/add/user', json=user)
        self.assertEqual(rt1.status_code, 201)

        pic = {
            "pic_id": "myid", "link": "/to/no/where"
        }
        rt2 = self.client.post('/pic/post', json=pic)
        self.assertEqual(rt2.status_code, 201)

        comment = {
            "ctext": "no comment", "username": "mgeni", "pic_id": "myid"
        }
        rt3 = self.client.post('/post/comment', json=comment)
        self.assertEqual(rt3.status_code, 201)

    def test_comment_get(self):
        self.test_comment_post()
        rt = self.client.get('/pic/myid/comments')
        self.assertEqual(rt.status_code, 200)

    def test_like_add(self):
        user = {
            "name": "mgeni", "username": "mgeni", "email": "r@e",
            "password": "123"
        }
        rt1 = self.client.post('/add/user', json=user)
        self.assertEqual(rt1.status_code, 201)

        pic = {
            "pic_id": "myid", "link": "/to/no/where"
        }
        rt2 = self.client.post('/pic/post', json=pic)
        self.assertEqual(rt2.status_code, 201)

        picLike = {
            "like": True, "username": "mgeni"
        }

        rt3 = self.client.post('/pic/myid/like', json=picLike)
        self.assertEqual(rt3.status_code, 201)

        rt3 = self.client.post('/pic/myid/like', json=picLike)
        self.assertEqual(rt3.status_code, 403)

    def test_like_pic_get(self):
        self.test_like_add()
        rt1 = self.client.get('/pic/myid/likes')

        self.assertEqual(rt1.status_code, 200)


if __name__ == '__main__':
    unittest.main()
