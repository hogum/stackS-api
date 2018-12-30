from .base_test import BaseTestCase
import json
from flask import jsonify


class AuthTestCases(BaseTestCase):
    """
    Tests user authentication

    """

    def test_get_registered_users(self):
        response = self.client.get('/api/v1/auth/register',
                                   data=self.user_data,
                                   content_type='application/json')
        res = json.loads(response.data.decode())

        self.assertTrue(isinstance(res, list),
                        msg="Fails to return user records as list")

        self.assertEqual(response.status_code, 200)

    def test_register_already_registered_user(self):

        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    content_type='application/json')
        res = json.loads(response.data.decode())

        res_msg = "Account exists. Maybe log in?"
        self.assertEqual(res,
                         res_msg,
                         msg="Fails to registration of existing account")

    def test_register_with_invalid_email(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Registers user with invalid email")

    def test_register_with_existing_username(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals.new",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 409,
                        msg="Fails. Registers user with existing username")

    def test_send_request_with_invalid_json(self):
        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    )
        res = json.loads(response.data.decode())
        res_msg = "Oops! That didn't work\
                Please provide a valid json header\t"
        self.assertEqual(res, res_msg,
                         msg="Fails to validate json headers")

    def test_get_users_records_are_instances(self):
        # Unneccessary
        response = self.client.get('/api/v1/auth/register',
                                   data=self.user_data,
                                   content_type='application/json')
        res = json.loads(response.data.decode())

        # Instances converted  to dict
        self.assertEqual(res[0].get('username'), (res[0]['username']),
                         msg="Fails to store user records as instances")

        self.assertEqual(response.status_code, 200)

    def test_login_registered_user(self):
        response = self.client.post('/api/v1/auth/login',
                                    data=self.user_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201,
                         msg="Fails to login registered user")

    def test_login_with_invalid_email(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Logs in user with invalid email")

    def test_login_with_incorrect_password(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals.milkable",
            password="password"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Logs in user with invalid password")

    def test_login_with_unregistered_email(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals.alien",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400,
                         msg="Fails. Logs in user with unknown email")

    def test_logged_in_user_can_log_out(self):

        self.client.post('/api/v1/auth/login',
                         data=self.user_data,
                         content_type='application/json')

        response = self.client.delete('/api/v1/auth/logout',
                                      headers=self.auth_header,
                                      data=self.user_data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201,
                         msg="Fails to logout user")
