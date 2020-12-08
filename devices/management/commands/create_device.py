import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '킥보드를 하나 생성합니다'

    def handle(self, *args, **options):
        device = Device()
        device.save()
