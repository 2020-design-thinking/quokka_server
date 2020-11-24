import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '강제로 모든 디바이스를 사용 가능하도록 만듭니다'

    def handle(self, *args, **options):
        for device in Device.objects.all():
            device.using = False
            device.save()
        self.stdout.write(self.style.SUCCESS('DONE'))
