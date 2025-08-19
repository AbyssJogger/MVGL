from django.core.management.base import BaseCommand
from games.models import Game

class Command(BaseCommand):
    help = 'Reset weekly views counter'

    def handle(self, *args, **kwargs):
        Game.objects.update(weekly_views=0)
        self.stdout.write(self.style.SUCCESS('Reset weekly views to zero.'))
