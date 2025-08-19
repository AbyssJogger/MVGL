from django.core.management.base import BaseCommand
from games.models import Game

class Command(BaseCommand):
    help = 'Reset monthly views counter'

    def handle(self, *args, **kwargs):
        Game.objects.update(monthly_views=0)
        self.stdout.write(self.style.SUCCESS('Reset monthly views to zero.'))
