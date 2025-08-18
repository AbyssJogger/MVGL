from django.urls import path

from pages.views import games_search_page_view, home_page_view


urlpatterns = [
    path('games/', games_search_page_view, name='games'),
    path('', home_page_view, name='home'),
]
