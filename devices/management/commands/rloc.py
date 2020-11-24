import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '쿼카의 위치를 주어진 영역 안에서 랜덤하게 바꿉니다'

    def add_arguments(self, parser):
        parser.add_argument('slat', type=float)
        parser.add_argument('slng', type=float)
        parser.add_argument('elat', type=float)
        parser.add_argument('elng', type=float)

    def handle(self, *args, **options):
        slat = min(options['slat'], options['elat'])
        slng = min(options['slng'], options['elng'])
        elat = max(options['slat'], options['elat'])
        elng = max(options['slng'], options['elng'])

        for device in Device.objects.all():
            device.lat = random.uniform(slat, elat)
            device.lng = random.uniform(slng, elng)
            device.save()

        self.stdout.write(self.style.SUCCESS('DONE'))
