import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '모든 킥보드 정보를 출력합니다'

    def handle(self, *args, **options):
        for device in Device.objects.all():
            self.stdout.write(self.style.SUCCESS('{} = ({}, {}) batt={} using={}'.format(device.pk, device.lat, device.lng
                                                                                       , device.battery, device.using)))

