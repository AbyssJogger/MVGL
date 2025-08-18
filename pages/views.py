from django.shortcuts import render

from games.models import Game


def home_page_view(req):
    return render(req, 'index.html', {'new_games': Game.objects.all()})
