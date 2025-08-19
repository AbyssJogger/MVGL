from django.contrib import admin

from .models import DeveloperAndPublisher, Game, GameReview, Genre, Platform


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'offline', 'online', 'rating']
    list_filter = ['genres', 'developer', 'publisher']
    search_fields = ['title', 'developer']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(DeveloperAndPublisher)
class DevAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ['game', 'score', 'author', 'status']

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name']
