from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import DeveloperAndPublisher, Game, Genre


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
        # Description too short
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
            rating=15,  # Invalid rating (too high)
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
        # This should not raise an error
        try:
            game.full_clean()
        except ValidationError:
            self.fail("Valid game raised ValidationError unexpectedly")

