from django.contrib import admin

from .models import DeveloperAndPublisher, Game, Genre

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'developer', 'rating']
    list_filter = ['genres', 'developer', 'publisher']
    search_fields = ['title', 'developer']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(DeveloperAndPublisher)
class DevAdmin(admin.ModelAdmin):
    list_display = ['name']
