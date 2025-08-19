# My Video Game List

A web app for keeping a list of video games you have played or are planning to play, inspired by [myanimelist.net](https://https://myanimelist.net/)

## disclaimer

The template used is not designed by me 

It's a template available at [colorlib.com](https://colorlib.com/)

## Run

use poetry for dependancy management

```sh
poetry install
poetry run manage.py makemigrations
poetry run manage.py migrate
poetry run manage.py runserver
```

## Management

add a cron job (or something similar) to reset the weekly and monthly views on games

```sh
poetry run manage.py reset_weekly_views
poetry run manage.py reset_monthly_views
```
