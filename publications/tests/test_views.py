from django.test import TestCase, Client
from users.models import User
from publications.models import Publication, Comment
from django.urls import reverse
from parameterized import parameterized


class TestViews(TestCase):
    def setUp(self):
        self.user_1 = User.create('test_email_1@gmail.com',
                                       'test_password_1',
                                       'test_first_name_1',
                                       'test_last_name_1')
        self.user_1.is_email_confirmed = True
        self.user_1.save()

        self.publication_1 = Publication(author=self.user_1,
                                         name='publication_1',
                                         image='static/img/image_1.png',
                                         description='description_1')
        self.publication_1.save()

        self.comment_1 = Comment.create(self.publication_1, self.user_1, 'text_1')

        self.user_2 = User.create('test_email_2@gmail.com',
                                       'test_password_2',
                                       'test_first_name_2',
                                       'test_last_name_2')
        self.user_2.save()

        self.client = Client()
        self.view_publication_1_url = reverse('view_publication', args=[1])
        self.view_user_1_url = reverse('view_user', args=[1])
        self.email_not_confirmed_url = reverse('email_not_confirmed')
        self.set_publication_mark_url = reverse('set_publication_mark', args=[1])
        self.delete_comment_url = reverse('delete_comment', args=[1])
        self.delete_publication_url = reverse('delete_publication', args=[1])

    @parameterized.expand([
        (reverse('view_publication', args=[1]), 'publications/view_publication.html'),
        (reverse('create_publication'), 'publications/create_publication.html'),
    ])
    def test_views_normal(self, url, template):
        signin = self.client.login(username='test_email_1@gmail.com', password='test_password_1')
        self.assertEqual(signin, True, msg='sign in failed')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)


    @parameterized.expand([
        (reverse('view_publication', args=[1])),
        (reverse('create_publication')),
        (reverse('delete_comment', args=[1])),
        (reverse('delete_publication', args=[1])),
        (reverse('set_publication_mark', args=[1])),
    ])
    def test_views_unconfirmed_email(self, url):
        signin = self.client.login(username='test_email_2@gmail.com', password='test_password_2')
        self.assertEqual(signin, True, msg='sign in failed')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.split('?')[0], self.email_not_confirmed_url)

    def test_like_publication(self):
        signin = self.client.login(username='test_email_1@gmail.com', password='test_password_1')

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        response = self.client.post(self.set_publication_mark_url, data={'value': 'like'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_publication_1_url)

        self.assertEqual(self.publication_1.likes.count(), 1)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

    def test_dislike_publication(self):
        signin = self.client.login(username='test_email_1@gmail.com', password='test_password_1')

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 0)

        response = self.client.post(self.set_publication_mark_url, data={'value': 'dislike'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_publication_1_url)

        self.assertEqual(self.publication_1.likes.count(), 0)
        self.assertEqual(self.publication_1.dislikes.count(), 1)

    def test_delete_comment(self):
        signin = self.client.login(username='test_email_1@gmail.com', password='test_password_1')

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                               publication=self.publication_1,
                                               text='text_1').exists())

        response = self.client.post(self.delete_comment_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_publication_1_url)

        self.assertFalse(Comment.objects.filter(author=self.user_1,
                                                publication=self.publication_1,
                                                text='text_1').exists())

    def test_delete_comment_wrong_login_user(self):
        self.user_2.is_email_confirmed = True
        self.user_2.save()
        signin = self.client.login(username='test_email_2@gmail.com', password='test_password_2')

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                               publication=self.publication_1,
                                               text='text_1').exists())

        response = self.client.post(self.delete_comment_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_publication_1_url)

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                                publication=self.publication_1,
                                                text='text_1').exists())

    def test_delete_publication(self):
        signin = self.client.login(username='test_email_1@gmail.com', password='test_password_1')

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                               publication=self.publication_1,
                                               text='text_1').exists())
        self.assertTrue(Publication.objects.filter(author=self.user_1,
                                                   name='publication_1',
                                                   image='static/img/image_1.png',
                                                   description='description_1',
                                                   ))

        response = self.client.post(self.delete_publication_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_user_1_url)

        self.assertFalse(Comment.objects.filter(author=self.user_1,
                                                publication=self.publication_1,
                                                text='text_1').exists())
        self.assertFalse(Publication.objects.filter(author=self.user_1,
                                                    name='publication_1',
                                                    image='static/img/image_1.png',
                                                    description='description_1',
                                                    ))

    def test_delete_publication_wrong_login_user(self):
        self.user_2.is_email_confirmed = True
        self.user_2.save()
        signin = self.client.login(username='test_email_2@gmail.com', password='test_password_2')

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                               publication=self.publication_1,
                                               text='text_1').exists())
        self.assertTrue(Publication.objects.filter(author=self.user_1,
                                                   name='publication_1',
                                                   image='static/img/image_1.png',
                                                   description='description_1',
                                                   ))

        response = self.client.post(self.delete_publication_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view_user_1_url)

        self.assertTrue(Comment.objects.filter(author=self.user_1,
                                               publication=self.publication_1,
                                               text='text_1').exists())
        self.assertTrue(Publication.objects.filter(author=self.user_1,
                                                   name='publication_1',
                                                   image='static/img/image_1.png',
                                                   description='description_1',
                                                   ))