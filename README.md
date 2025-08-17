# My Video Game List

A web app for keeping a list of video games you have played or are planning to play, inspired by [myanimelist.net](https://https://myanimelist.net/)

## Run

use poetry for dependancy management

```sh
poetry install
poetry run src/manage.py makemigrations <APPNAME>
poetry run src/manage.py migrate
poetry run src/manage.py runserver
```
