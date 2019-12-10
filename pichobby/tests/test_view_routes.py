import unittest
from base64 import b64encode
from pichobby import create_app, db
from pichobby.api.models import Users

global user, token, headers
user = {
    'name': "mgeni", 'username': "mgeni", 'password': "123",
    'email': "m@d"
}


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = Users('admin', 'admin', 'm@e', '123', True)
        db.session.add(user)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_home(self):
        rt = self.client.get('/')
        self.assertEqual(rt.status_code, 200)

    def test_a_login(self):
        global token
        upas = b64encode(("admin:123").encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': "Basic "+upas
        }
        rt2 = self.client.get('/login', headers=headers)
        token = rt2.data.decode().strip().strip("\"")
        self.assertEqual(rt2.status_code, 200)

    def test_b_add_user(self):
        global token, headers
        self.test_a_login()
        headers = {
            'Authorization': "Bearer " + token
        }
        rt1 = self.client.post('/add/user', json=user, headers=headers)
        self.assertEqual(rt1.status_code, 201)

    def test_c_get_users(self):
        self.test_b_add_user()
        rt1 = self.client.get('/guests')
        self.assertEqual(rt1.status_code, 200)

    def test_d_get_user(self):
        self.test_b_add_user()
        rt1 = self.client.get('/user/mgeni')
        self.assertEqual(rt1.status_code, 200)

    def test_e_post_pic(self):
        self.test_b_add_user()
        json1 = {
            'pic_id': "pic1", 'link': "/to/here"
        }
        json2 = {
            'pic_id': "pic2", 'link': "/to/here"
        }
        rt1 = self.client.post('/pic/post', json=json1, headers=headers)
        rt2 = self.client.post('/pic/post', json=json2, headers=headers)
        self.assertEqual(rt1.status_code, 201)
        self.assertEqual(rt2.status_code, 201)

    def test_f_get_pics(self):
        self.test_e_post_pic()
        rt1 = self.client.get('/pics')
        self.assertEqual(rt1.status_code, 200)

    def test_g_get_pic(self):
        self.test_e_post_pic()
        rt1 = self.client.get('/pic/pic1')
        self.assertEqual(rt1.status_code, 200)

    def test_h_post_comment(self):
        self.test_e_post_pic()
        json = {
            'ctext': "bad", 'username': "mgeni", 'pic_id': "pic1"
        }
        rt1 = self.client.post('/post/comment', json=json, headers=headers)
        self.assertEqual(rt1.status_code, 201)

    def test_i_get_comments(self):
        self.test_h_post_comment()
        rt1 = self.client.get('/pic/pic1/comments')
        self.assertEqual(rt1.status_code, 200)

    def test_j_post_like(self):
        self.test_e_post_pic()
        json = {
            'like': True, 'username': "mgeni"
        }
        rt1 = self.client.post('/pic/pic1/like', json=json, headers=headers)
        self.assertEqual(rt1.status_code, 201)

    def test_k_get_pic_like(self):
        self.test_j_post_like()
        rt1 = self.client.get('/pic/pic1/likes')
        self.assertEqual(rt1.status_code, 200)

    def test_l_get_user_likes(self):
        self.test_j_post_like()
        rt1 = self.client.get('/mgeni/mylikes')
        self.assertEqual(rt1.status_code, 200)


if __name__ == '__main__':
    unittest.main()
