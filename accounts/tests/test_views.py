from django.test import TestCase, Client
from django.urls import reverse
from parameterized import parameterized


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    @parameterized.expand(
        (
            (reverse('login'), 'accounts/login.html'),
            (reverse('register'), 'accounts/signup.html'),
        )
    )
    def test_views_normal(self, url, template):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)