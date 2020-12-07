import random
import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '모든 킥보드의 예약을 취소합니다'

    def handle(self, *args, **options):
        for device in Device.objects.all():
            device.reserve = None
            device.reserve_time = None
            device.save()
