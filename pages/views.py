from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from games.models import Game, Genre

def home_page_view(req):
    games = Game.objects.all()

    ctx = {
        'trending_games': games.order_by('-weekly_views', '-user_rating')[:6],
        'popular_games': games.order_by('-user_rating')[:6],
        'most_viewed_games': games.order_by('-monthly_views', '-total_views')[:6],
        'new_games': games.order_by('-release_date')[:6],
        'carousel_games': games.filter(rating__gt=9.5, user_rating__gt=9)[:3],
        'featured_games': games.order_by('?')[:5], # Random games to feature, definetely chagne this
        'page_keywords': ['videogame', 'entertainment', 'game', 'gamer', 'gaming', 'list', 'trailer', 'forums', 'community'],
        'page_description': 'A web app for keeping a list of video games you have played or are planning to play',
        'page_author': 'AbyssJogger',
        'page_name': 'home',
        'page_title': 'home',
    }
    return render(req, 'index.html', ctx)

def games_search_page_view(req):
    search_query = req.GET.get('search', '')
    genre_filter = req.GET.get('genre', '')
    orderby = req.GET.get('orderby', '')
    page = req.GET.get('page', 1)

    games = Game.objects.all()

    most_viewed_games = games.order_by('-total_views')[:6]

    if search_query:
        games = games.filter(title__icontains=search_query)

    if genre_filter:
        games = games.filter(genres__name__in=genre_filter)

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
        'most_viewed_games': most_viewed_games,
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
        'prev_page': games_page.number - 1,
        'curr_page': games_page.number,
        'is_paginated': games_page.has_other_pages(),
        'page_heading': 'Games',
        'page_name': 'games',
        'next_pages': [x for x in range(games_page.number + 1, games_page.number + 5 - int(bool(games_page.number - 1))) if x <= paginator.num_pages], # Have at the most 5 page numbers in pagination section
    }

    if search_query:
        ctx['page_heading'] = f'Search results for "{search_query}"'
        ctx['page_title'] = ctx['page_heading']

    return render(req, 'game_list.html', ctx)

def game_detail_view(req, pk):
    game = get_object_or_404(Game, pk=pk)
    reviews = game.reviews.select_related('author').all()

    ctx = {
        'game': game,
        'reviews': reviews,
        'page_title': f'{game.title}',
        'page_keywords': ['game', 'video game', 'review', game.title],
        'page_description': game.description,
        'page_author': 'AbyssJogger',
        'page_name': 'game_detail',
        'related_games': Game.objects.filter(genres__in=game.genres.all()).exclude(id=game.id).distinct()[:5]
    }
    return render(req, 'game_details.html', ctx)
