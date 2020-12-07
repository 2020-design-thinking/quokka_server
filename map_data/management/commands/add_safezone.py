import random

from django.core.management import BaseCommand

from map_data.models import SafeZone


class Command(BaseCommand):
    help = '보호구역을 추가합니다'

    def add_arguments(self, parser):
        parser.add_argument('lat', type=float)
        parser.add_argument('lng', type=float)
        parser.add_argument('radius', type=float)

    def handle(self, *args, **options):
        zone = SafeZone(lat=options['lat'], lng=options['lng'], radius=options['radius'])
        zone.save()
