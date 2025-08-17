from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import DeveloperAndPublisher, Game, Genre, GameReview


class DeveloperAndPublisherModelTest(TestCase):

    def test_str_method(self):
        dev = DeveloperAndPublisher.objects.create(name="Test Dev", is_dev=True, is_pub=False)
        self.assertEqual(str(dev), "Test Dev")

    def test_unique_name_constraint(self):
        DeveloperAndPublisher.objects.create(name="Unique Name", is_dev=True, is_pub=True)
        with self.assertRaises(Exception):
            # Creating another with the same name should fail
            DeveloperAndPublisher.objects.create(name="Unique Name", is_dev=False, is_pub=False)


class GenreModelTest(TestCase):

    def test_str_method(self):
        genre = Genre.objects.create(name="Action")
        self.assertEqual(str(genre), "Action")


class GameModelTest(TestCase):

    def setUp(self):
        self.dev = DeveloperAndPublisher.objects.create(name="Dev One", is_dev=True, is_pub=False)
        self.pub = DeveloperAndPublisher.objects.create(name="Pub One", is_dev=False, is_pub=True)
        self.genre = Genre.objects.create(name="RPG")

    def test_str_method(self):
        game = Game.objects.create(
            title="Test Game",
            description="A" * 150,
            publisher=self.pub,
            developer=self.dev,
            rating=7.5,
            cover="covers/test.jpg",
            release_date="2024-01-01",
        )
        game.genres.add(self.genre)
        self.assertEqual(str(game), "Test Game")

    def test_description_length_validator(self):
        game = Game(
            title="Short Desc Game",
            description="Too short",
            publisher=self.pub,
            developer=self.dev,
            rating=5,
            cover="covers/test.jpg",
            release_date="2024-01-01",
        )
        with self.assertRaises(ValidationError):
            game.full_clean()

    def test_rating_min_max_validator(self):
        game = Game(
            title="Invalid Rating Game",
            description="Valid description " * 10,
            publisher=self.pub,
            developer=self.dev,
            rating=15,
            cover="covers/test.jpg",
            release_date="2024-01-01",
        )
        with self.assertRaises(ValidationError):
            game.full_clean()

    def test_valid_game(self):
        game = Game(
            title="Valid Game",
            description="Valid description " * 10,
            publisher=self.pub,
            developer=self.dev,
            rating=8.5,
            cover="covers/test.jpg",
            release_date="2024-01-01",
        )
        try:
            game.full_clean()
        except ValidationError:
            self.fail("Valid game raised ValidationError unexpectedly")

    
class GameReviewModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='pass')
        self.dev = DeveloperAndPublisher.objects.create(name="Dev", is_dev=True)
        self.pub = DeveloperAndPublisher.objects.create(name="Pub", is_pub=True)
        self.game = Game.objects.create(
            title="Some Game",
            description="A" * 150,
            publisher=self.pub,
            developer=self.dev,
            rating=7.0,
            cover="covers/test.jpg",
            release_date="2025-01-01"
        )

    def test_str_method(self):
        review = GameReview.objects.create(
            game=self.game,
            author=self.user,
            score=9.5,
            recommend=True,
            text="This game is amazing!" * 5,
            status=GameReview.Status.FINISHED_MAIN
        )
        expected_str = f"{self.user}'s review on {self.game}"
        self.assertEqual(str(review), expected_str)

    def test_score_out_of_bounds(self):
        review = GameReview(
            game=self.game,
            author=self.user,
            score=11,  # invalid
            recommend=True,
            text="Great game!" * 5,
            status=GameReview.Status.COMPLETE
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_text_too_short(self):
        review = GameReview(
            game=self.game,
            author=self.user,
            score=7,
            recommend=False,
            text="Too short",
            status=GameReview.Status.DROPPED
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_invalid_status(self):
        review = GameReview(
            game=self.game,
            author=self.user,
            score=6,
            recommend=False,
            text="Not bad at all, decent experience." * 2,
            status=99  # invalid status
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_valid_review(self):
        review = GameReview(
            game=self.game,
            author=self.user,
            score=8.5,
            recommend=True,
            text="Very enjoyable game with a good storyline." * 3,
            status=GameReview.Status.PLAYING
        )
        try:
            review.full_clean()
        except ValidationError:
            self.fail("Valid GameReview raised ValidationError unexpectedly")
