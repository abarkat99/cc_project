from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from ..views import TopicCreateView
from ..forms import NewTopicForm


# Create your tests here.
User = get_user_model()


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='test', password='test')

    def test_new_topic_view_success_status_code(self):
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': 99, 'slug': 'random'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        self.client.force_login(self.user)
        resolver_match = resolve('/boards/1/django/new/')
        self.assertEquals(resolver_match.func.__name__, TopicCreateView.as_view().__name__)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        self.client.force_login(self.user)
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        self.client.force_login(self.user)
        url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
