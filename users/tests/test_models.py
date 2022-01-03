from django.test import TestCase
from users.models import User
from django.db.utils import IntegrityError
from parameterized import parameterized


class TestUserModel(TestCase):
    def setUp(self):
        self.test_user_1 = User(email='test_email_1@gmail.com',
                                password='test_password_1',
                                first_name='test_first_name_1',
                                last_name='test_last_name_1')
        self.test_user_1.save()

    def test_create_user(self):
        User.create('email_1@gmail.com', 'password_1', 'first_name_1', 'last_name_1')
        self.assertTrue(User.objects.filter(email='email_1@gmail.com').exists())

        with self.assertRaises(IntegrityError):
            User.create('email_1@gmail.com', 'password_2', 'first_name_2', 'last_name_2')

    def test_edit_profile(self):
        self.test_user_1.edit_profile(bio='new_bio')

        self.assertEqual(self.test_user_1.bio, 'new_bio')

        self.assertEqual(self.test_user_1.first_name, 'test_first_name_1')
        self.test_user_1.edit_profile(first_name='new_first_name')
        self.assertEqual(self.test_user_1.first_name, 'new_first_name')

    def test_edit_profile_few_changes(self):
        self.test_user_1.edit_profile(bio='test_bio',
                                      avatar='static/img/test_avatar.png',
                                      first_name='new_first_name',
                                      last_name='new_last_name')

        self.assertEqual(self.test_user_1.bio, 'test_bio')
        self.assertEqual(self.test_user_1.avatar, 'static/img/test_avatar.png')
        self.assertEqual(self.test_user_1.first_name, 'new_first_name')
        self.assertEqual(self.test_user_1.last_name, 'new_last_name')