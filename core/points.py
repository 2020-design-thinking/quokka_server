def calculate_points(dist):
    return int(dist / 0.1) * 8


def calculate_charge_points(device):
    if device.battery <= 0.3:
        return 150
    if device.battery <= 0.5:
        return 90
    return 0


def calculate_safety_points(safety_rate, dist):
    # dist = km
    if safety_rate < 3:
        return 0
    return int(safety_rate * 2)
