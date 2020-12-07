import random

from django.core.management import BaseCommand

from map_data.models import SafeZone


class Command(BaseCommand):
    help = '보호구역 반경을 전체적으로 수정합니다'

    def add_arguments(self, parser):
        parser.add_argument('radius', type=float)

    def handle(self, *args, **options):
        for zone in SafeZone.objects.all():
            zone.radius = options['radius']
            zone.save()
