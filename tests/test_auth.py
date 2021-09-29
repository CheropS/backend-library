"""File contains tests for auth api endpoints"""

from tests.base_test import TestHelloBooks
import json


class AuthTestCase(TestHelloBooks):
    """Test Class for all Auth endpoints"""

    def test_registration(self):
        """Tests Register User API endpoint"""
        empty_data = self.register_user(self.empty_user_data)
        self.assertEqual(empty_data.status_code, 400)
        no_email = self.register_user(self.user_data_no_email)
        self.assertEqual(no_email.status_code, 400)
        wrong_email = self.register_user(self.user_data_wrong_email)
        self.assertEqual(wrong_email.status_code, 400)
        long_email = self.register_user(self.user_data_long_email)
        self.assertEqual(long_email.status_code, 400)
        no_username = self.register_user(self.user_data_no_username)
        self.assertEqual(no_username.status_code, 400)
        long_username = self.register_user(self.user_data_long_username)
        self.assertEqual(long_username.status_code, 400)
        no_firstname = self.register_user(self.user_data_no_first_name)
        self.assertEqual(no_firstname.status_code, 400)
        long_firstname = self.register_user(self.user_data_long_first_name)
        self.assertEqual(long_firstname.status_code, 400)
        no_lastname = self.register_user(self.user_data_no_last_name)
        self.assertEqual(no_lastname.status_code, 400)
        long_lastname = self.register_user(self.user_data_long_last_name)
        self.assertEqual(long_lastname.status_code, 400)
        no_password = self.register_user(self.user_data_no_password)
        self.assertEqual(no_password.status_code, 400)
        short_password = self.register_user(self.user_data_short_password)
        self.assertEqual(short_password.status_code, 400)
        register = self.register_user(self.user_data)
        self.assertEqual(register.status_code, 201)
        email_exists = self.register_user(self.user_data)
        self.assertEqual(email_exists.status_code, 409)
        username_exists = self.register_user(self.user_data2)
        self.assertEqual(username_exists.status_code, 409)
        no_confirm = self.register_user(self.user_data_no_confirm)
        self.assertEqual(no_confirm.status_code, 400)
        pass_mismatch = self.register_user(self.user_data_password_mismatch)
        self.assertEqual(pass_mismatch.status_code, 400)

    def test_login(self):
        """Tests Login User API endpoint"""
        self.register_user(self.user_data)
        user_not_exist = self.login_user(self.login_data_user_not_exist)
        self.assertEqual(user_not_exist.status_code, 404)
        password_mismatch = self.login_user(self.login_data_password_mismatch)
        self.assertEqual(password_mismatch.status_code, 401)
        login = self.login_user(self.login_data)
        self.assertEqual(login.status_code, 200)
        login2 = self.login_user(self.login_data)
        self.assertEqual(login2.status_code, 200)
        logout = self.logout_user(login)
        self.assertEqual(logout.status_code, 200)
        logout2 = self.logout_user(login2)
        self.assertEqual(logout2.status_code, 200)