import random

from django.core.management import BaseCommand

from devices.models import Device
from users.models import User


class Command(BaseCommand):
    help = '모든 유저 정보를 출력합니다'

    def handle(self, *args, **options):
        for user in User.objects.all():
            self.stdout.write(self.style.SUCCESS('{}, {} email={} last_drive={}'.format(user.first_name,
                                                                                        user.last_name,
                                                                                        user.email, user.last_drive)))
