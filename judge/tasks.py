from celery import shared_task

from judge.models import DrivingImage


@shared_task
def judge_image(pk):
    image = DrivingImage.objects.get(pk=pk)

    # TODO
