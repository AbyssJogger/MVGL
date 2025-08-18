from django.urls import path

from pages.views import game_detail_view, games_search_page_view, home_page_view


urlpatterns = [
    path('games/<int:pk>', game_detail_view, name='game_details'),
    path('games/', games_search_page_view, name='games'),
    path('', home_page_view, name='home'),
]
