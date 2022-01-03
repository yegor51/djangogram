from django.test import TestCase
from publications.models import Publication, Comment
from users.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user_1 = User(email='test_email_1@gmail.com',
                           password='test_password_1',
                           first_name='test_first_name_1',
                           last_name='test_last_name_1')
        self.user_1.is_email_confirmed = True
        self.user_1.save()

        self.publication_1 = Publication(author=self.user_1,
                                         name='publication_2',
                                         image='static/img/image_2.png',
                                         description='description_2')

        self.publication_1.save()

        self.user_2 = User(email='test_email_2@gmail.com',
                           password='test_password_2',
                           first_name='test_first_name_2',
                           last_name='test_last_name_2')
        self.user_2.is_email_confirmed = True
        self.user_2.save()

    def test_create_publication(self):
        Publication.create(self.user_1,
                                       'publication_2',
                                       'static/img/image_2.png',
                                       'description_2')

        self.assertTrue(Publication.objects.filter(name='publication_2',
                                                   image='static/img/image_2.png',
                                                   description='description_2').exists())

    def test_set_like(self):
        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        self.publication_1.set_like(self.user_1)

        self.assertEqual(self.publication_1.likes.count(), 1)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        self.publication_1.set_like(self.user_2)

        self.assertEqual(self.publication_1.likes.count(), 2)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

    def test_set_dislike(self):
        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        self.publication_1.set_dislike(self.user_1)

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 1)

        self.publication_1.set_dislike(self.user_2)

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 2)

    def test_remove_mark(self):
        self.publication_1.set_like(self.user_1)
        self.publication_1.remove_any_mark(self.user_1)

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        self.publication_1.set_dislike(self.user_1)
        self.publication_1.remove_any_mark(self.user_1)

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

    def test_create_comment(self):
        Comment.create(self.publication_1,
                               self.user_1,
                               'text_1')

        self.assertTrue(Comment.objects.filter(publication=self.publication_1,
                                               author=self.user_1,
                                               text='text_1').exists())
