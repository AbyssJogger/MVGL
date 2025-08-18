from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from games.models import Game, Genre

def home_page_view(req):
    games = Game.objects.all()

    ctx = {
        'new_games': games.order_by('-release_date'),
        'best_games': games.filter(rating__gt=9.5),
        # Random games to feature, definetely chagne this
        'featured_games': games.order_by('?')[:5],
        'page_keywords': ['videogame', 'entertainment', 'game', 'gamer', 'gaming', 'list', 'trailer', 'forums', 'community'],
        'page_description': 'A web app for keeping a list of video games you have played or are planning to play',
        'page_author': 'AbyssJogger',
        'page_name': 'home',
    }
    return render(req, 'index.html', ctx)

def games_search_page_view(req):
    search_query = req.GET.get('search', '')
    genre_filter = req.GET.get('genre', '')
    orderby = req.GET.get('orderby', '')
    page = req.GET.get('page', 1)

    games = Game.objects.all()

    if search_query:
        games = games.filter(title__icontains=search_query)

    if genre_filter:
        games = games.filter(genres__name=genre_filter)

    if orderby:
        games = games.order_by(orderby)

    games = games.distinct()
    genres = Genre.objects.all()

    paginator = Paginator(games, 16)

    try:
        games_page = paginator.page(page)
    except PageNotAnInteger:
        games_page = paginator.page(1)
    except EmptyPage:
        games_page = paginator.page(paginator.num_pages)

    ctx = {
        'games': games_page,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'order_by': orderby,
        'page_title': 'MVGL - Games',
        'page_keywords': ['games', 'video games', 'search', 'filter'],
        'page_description': 'Browse and filter video games',
        'page_author': 'AbyssJogger',
        'paginator': paginator,
        'current_page': games_page.number,
        'is_paginated': games_page.has_other_pages(),
        'page_heading': 'Games',
        'page_name': 'games',
    }

    if search_query:
        ctx['page_heading'] = f'Search results for "{search_query}"'
        ctx['page_title'] = ctx['page_heading'] + ' - MVGL'

    return render(req, 'game_list.html', ctx)
