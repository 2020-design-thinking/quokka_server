from drive.models import LocationSample

from math import cos, asin, sqrt, pi


# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))


def calculate_charge(drive):
    locations = LocationSample.objects.filter(drive=drive)
    total_dist = 0
    for i in range(1, len(locations)):
        total_dist += distance(float(locations[i - 1].lat), float(locations[i - 1].lng), float(locations[i].lat), float(locations[i].lng))

    return int(400 + total_dist * 800)
