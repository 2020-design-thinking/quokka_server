def calculate_points(dist):
    return int(dist / 0.1) * 8


def calculate_charge_points(device):
    if device.battery <= 0.3:
        return 100
    return 0


def calculate_safety_points(safety_rate, dist):
    # dist = km
    if safety_rate >= 4.5:
        return int(dist) * 100
    elif safety_rate >= 4:
        return int(dist) * 30
    elif safety_rate >= 3:
        return int(dist) * 10
    return 0
