from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board
from ..views import TopicListView


# Create your tests here.


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99, 'slug': 'random-slug'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        resolver_match = resolve('/boards/1/django/')
        self.assertEquals(resolver_match.func.__name__, TopicListView.as_view().__name__)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk, 'slug': self.board.slug})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk, 'slug': self.board.slug})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
