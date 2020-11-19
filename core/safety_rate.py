from judge.models import SafetyScore


def calculate_safety_rate(drive):
    scores = SafetyScore.objects.filter(drive=drive)

    average = 0
    for score in scores:
        average += score.score
    average /= len(scores)

    return round(average, 1)
