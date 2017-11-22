import sys
import unittest


sys.path.append(sys.path[0] + "/..")


from app import app


class MembershipTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, username='user', password='password'):
        rv = self.app.post('/membership/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        return rv

    def logout(self):
        rv = self.app.post('/membership/logout', follow_redirects=True)
        return rv

    def test_login(self):
        rv = self.app.get('/membership/login')
        assert 200 == rv.status_code
        assert b'Login' in rv.data
        assert b'Username:' in rv.data
        assert b'Password:' in rv.data

        rv = self.login('user', 'wrong_password')
        assert 200 == rv.status_code
        assert b'fail' in rv.data

        rv = self.login()
        with self.app.session_transaction() as sess:
            assert 200 == rv.status_code
            assert 'success' in rv.data.decode('UTF-8')
            assert sess['username'] == 'user'

    def test_logout(self):
        self.login()
        with self.app.session_transaction() as sess:
            assert not not sess

        rv = self.app.get('/membership/logout', follow_redirects=True)
        assert 405 == rv.status_code

        rv = self.logout()
        assert 200 == rv.status_code
        assert b'success' in rv.data
        with self.app.session_transaction() as sess:
            assert not sess

    def test_profile(self):
        self.login()
        rv = self.app.get('/membership/profile')
        assert 200 == rv.status_code
        assert b'profile' in rv.data


if __name__ == '__main__':
    unittest.main()
