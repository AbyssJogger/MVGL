from django.db import models

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

class Game(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=4096, validators=[LengthRangeValidator(100, 2000)])
    publisher = models.ForeignKey(DeveloperAndPublisher, on_delete=models.SET_NULL, null=True, related_name='released_games')
    developer = models.ForeignKey(DeveloperAndPublisher, on_delete=models.SET_NULL, null=True, related_name='published_games')
    rating = models.FloatField(validators=[MinMaxValidator(0, 10)])
    cover = models.ImageField(upload_to='%Y/%m/cover')
    banner = models.ImageField(upload_to='%Y/%m/banner', null=True, blank=True)
    release_date = models.DateField()
    version = models.CharField(max_length=15, blank=True, default='1.0.0')
    genres = models.ManyToManyField(Genre, related_name='games')

    def __str__(self):
        return str(self.title)
