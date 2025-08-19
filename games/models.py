from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.choices import BlankChoiceIterator

from .validators import LengthRangeValidator, MinMaxValidator


class DeveloperAndPublisher(models.Model):
    name = models.CharField(max_length=250, unique=True)
    is_dev = models.BooleanField(default=False)
    is_pub = models.BooleanField(default=False)
    opened_at = models.DateField(null=True, blank=True)
    closed_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Platform(models.Model):
    company = models.ManyToManyField(DeveloperAndPublisher, related_name='released_consoles')
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=4096, validators=[LengthRangeValidator(100, 2000)])
    publisher = models.ManyToManyField(DeveloperAndPublisher, related_name='released_games')
    developer = models.ManyToManyField(DeveloperAndPublisher, related_name='published_games')
    rating = models.FloatField(validators=[MinMaxValidator(0, 10)])
    user_rating = models.FloatField(validators=[MinMaxValidator(0, 10)])
    cover = models.ImageField(upload_to='%Y/%m/cover')
    banner = models.ImageField(upload_to='%Y/%m/banner', null=True, blank=True)
    release_date = models.DateField()
    version = models.CharField(max_length=15, blank=True, default='1.0.0')
    genres = models.ManyToManyField(Genre, related_name='games')
    gameplay_duration = models.FloatField(validators=[MinValueValidator(0)])
    total_views = models.PositiveBigIntegerField(default=0, blank=True)
    monthly_views = models.PositiveBigIntegerField(default=0, blank=True)
    weekly_views = models.PositiveBigIntegerField(default=0, blank=True)
    platforms = models.ManyToManyField(Platform, related_name='supporteded_games')
    online = models.BooleanField(default=False)
    offline = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('game_details', args=[str(self.id)])


class GameReview(models.Model):
    class Status(models.IntegerChoices):
        PLANNING = 0, 'Planning to play'
        PLAYING = 1, 'Playing'
        FINISHED_MAIN = 2, 'Finished main game'
        COMPLETE = 3, 'Completed'
        DROPPED = 4, 'Dropped'
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='game_reviews')
    score = models.FloatField(validators=[MinMaxValidator(0, 10)])
    recommend = models.BooleanField(default=True)
    text = models.TextField(validators=[LengthRangeValidator(20, 2000)])
    status = models.PositiveIntegerField(choices=Status.choices, default=Status.PLANNING)
    created_at = models.DateTimeField(auto_now_add=True)
    platforms = models.ManyToManyField(Platform, related_name='related_reviews')

    def __str__(self):
        return str(self.author) + '\'s review on ' + str(self.game)
