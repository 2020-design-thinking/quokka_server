import random

from django.core.management import BaseCommand

from devices.models import Device


class Command(BaseCommand):
    help = '강제로 모든 디바이스의 사용 여부를 랜덤으로 설정합니다'

    def handle(self, *args, **options):
        for device in Device.objects.all():
            if not device.using:
                device.using = random.random() > 0.5
                device.save()
        self.stdout.write(self.style.SUCCESS('DONE'))
