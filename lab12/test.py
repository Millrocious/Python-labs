import unittest

from flask_login import current_user
from flask_testing import TestCase

from app import create_app, db
from app.auth.models import User
from app.todo.models import Category, Task
from datetime import datetime


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app(config_name='test')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User(username="test",
                            email="test@email.com",
                            password="test"))
        db.session.add(Category(name="school"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )
        self.assertIn(b'You have been logged in!', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="test2@email.com",
                      password="test2",
                      remember="y"),
            follow_redirects=True
        )
        self.assertIn(b'Login unsuccessful. Please check username and password', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        response = self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)

    def test_registration(self):
        response = self.client.post('/register',
                                    data=dict(
                                        username='new_test1',
                                        email='test1@email.com',
                                        password='new_test1',
                                        confirm_password='new_test1'
                                    ),
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created', response.data)

        response = self.client.post(
            '/login',
            data=dict(email="test1@email.com",
                      password="new_test1",
                      remember="y"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_user.username, "new_test1")

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        self.assertTrue(current_user.is_anonymous)

        # Ensure that logout page requires user login

    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_create_category(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/category/create',
                                    data=dict(
                                        name="homework"
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Category successfully added', response.data)

    def test_create_task(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/task/create',
                                    data=dict(
                                        title='Test task',
                                        message='task desc',
                                        deadline='2022-12-15',
                                        priority=1,
                                        progress=1,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully created', response.data)

    def test_list_of_tasks(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/task/create',
                                    data=dict(
                                        title='Test task',
                                        description='task desc',
                                        deadline='2022-12-15',
                                        priority=1,
                                        progress=1,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully created', response.data)

        response = self.client.get('/task/list')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test task', response.data)

    def test_detail_task(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/task/create',
                                    data=dict(
                                        title='Test task',
                                        description='task desc',
                                        deadline='2022-12-15',
                                        priority=1,
                                        progress=1,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully created', response.data)

        response = self.client.get('/task/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'task desc', response.data)

    def test_task_update(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/task/create',
                                    data=dict(
                                        title='Test task',
                                        description='task desc',
                                        deadline='2022-12-15',
                                        priority=1,
                                        progress=1,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully created', response.data)

        response = self.client.post('/task/1/update',
                                    data=dict(
                                        title='updated test task',
                                        description='updated task desc',
                                        deadline='2022-12-15',
                                        priority=2,
                                        progress=2,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully updated', response.data)

        response = self.client.get('/task/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'updated test task', response.data)

    def test_task_delete(self):
        self.client.post(
            '/login',
            data=dict(email="test@email.com",
                      password="test",
                      remember="y"),
            follow_redirects=True
        )

        response = self.client.post('/task/create',
                                    data=dict(
                                        title='Test task',
                                        description='task desc',
                                        deadline='2022-12-15',
                                        priority=1,
                                        progress=1,
                                        category=1
                                    ),
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task successfully created', response.data)

        response = self.client.post('/task/1/delete',
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully deleted!', response.data)


if __name__ == '__main__':
    unittest.main()
