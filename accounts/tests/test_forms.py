from django.test import TestCase
from users.models import User
from parameterized import parameterized
from accounts.forms import UserLoginForm, UserRegisterForm


class TestUserLoginForm(TestCase):
    def setUp(self):
        self.test_user = User.create('test_email@gmail.com', 'test_password', 'test_first_name', 'test_last_name')
        self.test_not_active_user = User.create('test_email_2@gmail.com',
                                                     'test_password_2',
                                                     'test_first_name_2',
                                                     'test_last_name_2',
                                                     is_active=False)

    def test_correct_input(self):
        form = UserLoginForm(data={'email': 'test_email@gmail.com',
                                   'password': 'test_password'})
        self.assertTrue(form.is_valid())

    @parameterized.expand((
            ('wrong_email@gmail.com', 'test_password'),
            ('test_email@gmail.com', 'wrong_password'),
            ('test_email_2@gmail.com', 'test_password_2'),
    ))
    def test_incorrect_input(self, email, password):
        form = UserLoginForm(data={'email': email,
                                   'password': password})
        self.assertFalse(form.is_valid())


class TestUserRegisterForm(TestCase):
    def setUp(self):
        self.test_user = User.create('test_email@gmail.com', 'test_password', 'test_first_name', 'test_last_name')

    def test_form_correct_data(self):
        form = UserRegisterForm(data={'email': 'test_email_2@gmail.com',
                                      'password': 'test_password_2',
                                      'password_confirm': 'test_password_2',
                                      'first_name': 'test_first_name_2',
                                      'last_name': 'test_last_name_2'})

        self.assertTrue(form.is_valid())

    @parameterized.expand((
            (
                    'test_email_2@gmail.com',
                    'test_password_1',
                    'test_password_2',
                    'test_first_name',
                    'test_last_name',
            ),
            (
                    'test_email@gmail.com',
                    'test_password_1',
                    'test_password_1',
                    'test_first_name',
                    'test_last_name',
             ),
    ))
    def test_form_incorrect_data(self, email, password, password_confirm, first_name, last_name):
        form = UserRegisterForm(data={'email': email,
                                      'password': password,
                                      'password_confirm': password_confirm,
                                      'first_name': first_name,
                                      'last_name': last_name})

        self.assertFalse(form.is_valid())