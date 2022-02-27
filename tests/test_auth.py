from tests.base import BaseTest
from tests.utils import json_format, post_api


class TestRegister(BaseTest):
    def test_register_with_weak_password(self):
        res = post_api(self, '/api/v1/auth/register', data=self.weak_data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['message'], 'A vulnerable password.')

    def test_register_with_strong_password(self):
        res = post_api(self, '/api/v1/auth/register', data=self.strong_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Register successful.')

    def test_register_with_email_none(self):
        data = json_format(email=None, password=self.strong_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid input.')

    def test_register_with_password_none(self):
        data = json_format(email=self.email, password=None)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid input.')

    def test_register_with_valid_credentials_and_irrelevant_attribute(self):
        data = json_format(email=self.email, password=self.strong_password,
                           irrelevant_attribute='irrelevant_attribute')
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Register successful.')

    def test_register_with_invalid_email(self):
        data = json_format(email='example@example',
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid Email.')

    def test_register_with_duplicated_email(self):
        post_api(self, '/api/v1/auth/register', data=self.strong_data)
        res = post_api(self, '/api/v1/auth/register', data=self.strong_data)
        self.assertEqual(res['meta']['code'], 409)
        self.assertEqual(res['response']['message'], 'Already exists.')

    def test_register_with_leaked_password(self):
        data = json_format(email=self.email, password=self.leaked_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['message'], 'A vulnerable password.')

    def test_register_if_password_is_the_same_as_password(self):
        data = json_format(email=self.email, password=self.email)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['message'], 'A vulnerable password.')


class TestLogin(BaseTest):
    def test_login_with_user_does_not_exist(self):
        res = post_api(self, '/api/v1/auth/login', data=self.weak_data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')

    def test_login_with_valid_credentials(self):
        res = post_api(self, '/api/v1/auth/login',
                       data=self.registered_user_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertRegexpMatches(
            res['response']['message'], 'Login successful.')

    def test_login_with_wrong_password(self):
        data = json_format(email=self.registered_user_email,
                           password=self.wrong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')

    def test_login_with_irrelevant_attribute(self):
        data = json_format(
            email=self.registered_user_email,
            password=self.strong_password,
            irrelevant_attribute='irrelevant_attribute')
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertRegexpMatches(
            res['response']['message'], 'Login successful.')

    def test_login_with_injection_email(self):
        data = json_format(email=self.injection_email,
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')

    def test_login_with_injection_code_in_email(self):
        data = json_format(email=self.injection_code,
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')

    def test_login_with_injection_password(self):
        data = json_format(email=self.registered_user_email,
                           password=self.injection_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')

    def test_login_with_injection_code(self):
        data = json_format(email=self.registered_user_email,
                           code=self.injection_code)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid input')

    def test_login_with_path_traversal_attack(self):
        data = json_format(email=self.path_traversal,
                           password=self.path_traversal)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['message'], 'Invalid credentials.')