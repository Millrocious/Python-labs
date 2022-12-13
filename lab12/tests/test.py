import unittest

from flask_testing import TestCase

from app import db, create_app
from app.auth.models import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        test_app = create_app()
        return test_app

    def setUp(self):
        db.create_all()
        db.session.add(User(username="test", email="test@min.com", password="test"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to my homepage', response.data)

    def test_404(self):
        response = self.client.get('/homee', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_account(self):
        response = self.client.get('/account', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="tesst@min.com", password="test"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful. Please check username and password', response.data)



if __name__ == '__main__':
    unittest.main()