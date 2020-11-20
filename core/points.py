def calculate_points(dist):
    return int(dist / 100) * 8


def calculate_charge_points(device):
    if device.battery <= 0.3:
        return 100
    return 0


def calculate_safety_points(safety_rate):
    if safety_rate == 5:
        return 100
    elif safety_rate >= 4:
        return 30
    elif safety_rate >= 3:
        return 10
    return 0
