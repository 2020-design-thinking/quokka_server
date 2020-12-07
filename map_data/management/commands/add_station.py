import random

from django.core.management import BaseCommand

from map_data.models import Station


class Command(BaseCommand):
    help = '충전소를 추가합니다'

    def add_arguments(self, parser):
        parser.add_argument('lat', type=float)
        parser.add_argument('lng', type=float)

    def handle(self, *args, **options):
        station = Station(lat=options['lat'], lng=options['lng'])
        station.save()
