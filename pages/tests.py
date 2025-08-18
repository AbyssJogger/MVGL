from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from games.models import Game, Genre, DeveloperAndPublisher, GameReview


class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create developer and publisher
        cls.dev = DeveloperAndPublisher.objects.create(name="Dev Test", is_dev=True)
        cls.pub = DeveloperAndPublisher.objects.create(name="Pub Test", is_pub=True)

        # Create genres
        cls.genre1 = Genre.objects.create(name="Action")
        cls.genre2 = Genre.objects.create(name="RPG")

        # Create 20 games for pagination test
        for i in range(20):
            game = Game.objects.create(
                title=f"Game {i}",
                description="Valid description " * 10,
                publisher=cls.pub,
                developer=cls.dev,
                rating=7.5 + (i * 0.1),
                cover="covers/test.jpg",
                release_date="2024-01-01"
            )
            # Add genres to some games
            if i % 2 == 0:
                game.genres.add(cls.genre1)
            else:
                game.genres.add(cls.genre2)

    def test_home_page_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        # Check context keys exist
        self.assertIn('new_games', response.context)
        self.assertIn('best_games', response.context)
        self.assertIn('featured_games', response.context)

        # Check ordering for new_games (descending by release_date)
        new_games = response.context['new_games']
        self.assertTrue(all(new_games[i].release_date >= new_games[i+1].release_date for i in range(len(new_games)-1)))

        # Check best_games rating > 9.5
        best_games = response.context['best_games']
        self.assertTrue(all(game.rating > 9.5 for game in best_games))

    def test_games_search_page_view_basic(self):
        url = reverse('games')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_list.html')

        # Check paginator keys
        self.assertIn('games', response.context)
        self.assertIn('paginator', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])

        # Default page should contain 16 games (page size)
        self.assertEqual(len(response.context['games']), 16)

    def test_games_search_page_pagination(self):
        url = reverse('games')

        # Request page 2
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['games'].number, 2)
        self.assertTrue(response.context['is_paginated'])
        # Should contain remaining 4 games (20 total - 16 on page 1)
        self.assertEqual(len(response.context['games']), 4)

    def test_games_search_page_filter_genre(self):
        url = reverse('games')

        # Filter by genre Action (genre1)
        response = self.client.get(url, {'genre': 'Action'})
        self.assertEqual(response.status_code, 200)
        games = response.context['games']
        self.assertTrue(all(self.genre1 in game.genres.all() for game in games))

    def test_games_search_page_search_query(self):
        url = reverse('games')

        # Search for games with "Game 1" in title (should match "Game 1", "Game 10", "Game 11", etc)
        response = self.client.get(url, {'search': 'Game 1'})
        self.assertEqual(response.status_code, 200)
        games = response.context['games']
        self.assertTrue(all('Game 1' in game.title for game in games))

    def test_games_search_page_orderby(self):
        url = reverse('games')

        # Order by rating ascending
        response = self.client.get(url, {'orderby': 'rating'})
        self.assertEqual(response.status_code, 200)
        games = list(response.context['games'])
        self.assertEqual(games, sorted(games, key=lambda g: g.rating))

        # Order by rating descending
        response_desc = self.client.get(url, {'orderby': '-rating'})
        games_desc = list(response_desc.context['games'])
        self.assertEqual(games_desc, sorted(games_desc, key=lambda g: g.rating, reverse=True))


class GameDetailViewTest(TestCase):

    def setUp(self):
        # Create developer and publisher
        self.dev = DeveloperAndPublisher.objects.create(name="DevTest", is_dev=True)
        self.pub = DeveloperAndPublisher.objects.create(name="PubTest", is_pub=True)
        
        # Create genres
        self.genre1 = Genre.objects.create(name="RPG")
        self.genre2 = Genre.objects.create(name="Action")

        # Create a game
        self.game = Game.objects.create(
            title="Test Game",
            description="This is a test game description which is sufficiently long to pass validators.",
            publisher=self.pub,
            developer=self.dev,
            rating=8.5,
            cover="covers/test.jpg",
            release_date="2024-01-01",
            version="1.0.0"
        )
        self.game.genres.add(self.genre1, self.genre2)

        # Create a user for reviews
        self.user = get_user_model().objects.create_user(username='reviewer', password='pass1234')

        # Create some reviews
        self.review1 = GameReview.objects.create(
            game=self.game,
            author=self.user,
            score=9.0,
            recommend=True,
            text="Great game! Loved the story and gameplay.",
            status=GameReview.Status.FINISHED_MAIN,
        )
        self.review2 = GameReview.objects.create(
            game=self.game,
            author=self.user,
            score=7.5,
            recommend=False,
            text="Good, but had some issues with bugs.",
            status=GameReview.Status.PLAYING,
        )

    def test_game_details_status_code(self):
        url = reverse('game_details', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_game_details_uses_correct_template(self):
        url = reverse('game_details', args=[self.game.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'game_details.html')

    def test_game_details_context(self):
        url = reverse('game_details', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.context['game'], self.game)
        self.assertIn(self.review1, response.context['reviews'])
        self.assertIn(self.review2, response.context['reviews'])

    def test_game_details_404_for_invalid_id(self):
        url = reverse('game_details', args=[9999])  # Assuming this ID does not exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

