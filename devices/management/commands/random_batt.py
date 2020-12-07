import random
import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '킥보드 배터리를 랜덤으로 설정합니다'

    def handle(self, *args, **options):
        for device in Device.objects.all():
            device.battery = random.random()
            device.save()
