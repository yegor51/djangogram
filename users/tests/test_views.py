from django.test import TestCase, Client
from users.models import User
from django.urls import reverse
from parameterized import parameterized


class TestViews(TestCase):
    def setUp(self):
        self.test_user = User.create_user('test_email_1@gmail.com',
                                          'test_password_1',
                                          'test_first_name_1',
                                          'test_last_name_1')
        self.test_user.is_email_confirmed = True
        self.test_user.save()

        self.test_unconfirmed_user = User.create_user('test_email_2@gmail.com',
                                                      'test_password_2',
                                                      'test_first_name_2',
                                                      'test_last_name_2')

        self.client = Client()
        self.user_view_url = reverse('view_user', args=(self.test_user.id,))
        self.unconfirmed_user_view_url = reverse('view_user',
                                                 args=(self.test_unconfirmed_user.id,))
        self.my_profile_url = reverse('my_profile')
        self.email_not_confirmed_url = reverse('email_not_confirmed')

    def test_user_login(self, email='test_email_1@gmail.com', password='test_password_1'):
        signin = self.client.login(username=email, password=password)
        self.assertEqual(signin, True, msg='sign in failed')
        return signin

    @parameterized.expand(
        [
            (reverse('view_user', args=(1,)),),
            (reverse('view_all_users'),),
            (reverse('my_profile'),),
        ]
    )
    def test_views_with_unconfirmed_email(self, url):
        self.test_user_login('test_email_2@gmail.com', 'test_password_2')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.split('?')[0], self.email_not_confirmed_url)

    @parameterized.expand(
        (
            (reverse('view_user', args=(1,)), 'users/view_user.html'),
            (reverse('view_all_users'), 'users/all_users.html'),
        )
    )
    def test_views_normal(self, url, template):
        self.test_user_login()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_view_my_profile(self):
        self.test_user_login()

        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.user_view_url)

        self.test_unconfirmed_user.is_email_confirmed = True
        self.test_unconfirmed_user.save()
        self.test_user_login('test_email_2@gmail.com', 'test_password_2')

        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.unconfirmed_user_view_url)