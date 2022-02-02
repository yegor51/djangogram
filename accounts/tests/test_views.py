from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from users.models import User
from unittest.mock import MagicMock
from parameterized import parameterized


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.create('test_email@gmail.com', 'test_password', 'test_first_name', 'test_last_name')

        self.login_view_url = reverse('login')
        self.register_view_url = reverse('register')
        self.logout_view_url = reverse('logout')
        self.send_confirmation_link_url = reverse('send_activation_link')

        User.send_confirmation_link = MagicMock()

    @parameterized.expand(
        (
            (reverse('login'), 'accounts/login.html'),
            (reverse('register'), 'accounts/signup.html'),
            (reverse('email_not_confirmed'), 'accounts/email_not_confirmed.html'),
        )
    )
    def test_views_normal(self, url, template):
        self.client.login(username='test_email@gmail.com', password='test_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_user_log_in(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.post(self.login_view_url, {
            'email': 'test_email@gmail.com',
            'password': 'test_password',
        })
        self.assertTrue(response.status_code, 302)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    @parameterized.expand((
            ('wrong_email@gmail.com', 'test_password'),
            ('test_email@gmail.com', 'wrong_password'),
    ))
    def test_incorrect_user_log_in(self, email, password):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.post(self.login_view_url, {
            'email': email,
            'password': password,
        })
        self.assertTrue(response.status_code, 200)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_user_register(self):
        response = self.client.post(self.register_view_url, {
            'email': 'test_email2@gmail.com',
            'password': 'test_password',
            'password_confirm': 'test_password',
            'first_name': 'first_name',
            'last_name': 'last_name',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test_email2@gmail.com',
                                            first_name='first_name',
                                            last_name='last_name').exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.assertEqual(len(User.send_confirmation_link.call_args_list), 1)

    @parameterized.expand((
            ('test_email@gmail.com', 'test_password', 'test_password', 'first_name', 'last_name'),
            ('test_email2@gmail.com', 'test_password', 'test_password_2', 'first_name', 'last_name'),
    ))
    def test_incorrect_user_register(self, email, password, password_confirm, first_name, last_name):
        response = self.client.post(self.register_view_url, {
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
            'first_name': first_name,
            'last_name': last_name,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=email,
                                             first_name=first_name,
                                             last_name=last_name).exists())
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertEqual(len(User.send_confirmation_link.call_args_list), 0)

    def test_logout_view(self):
        self.client.login(username='test_email@gmail.com', password='test_password')
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        response = self.client.get(self.logout_view_url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_send_confirmation_link(self):
        self.client.login(username='test_email@gmail.com', password='test_password')

        response = self.client.post(self.send_confirmation_link_url)

        self.assertEqual(len(User.send_confirmation_link.call_args_list), 1)