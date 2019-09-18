import math


EARTH_RADIUS = 6371


def gcd(point1, point2):
    """
    Great Circle Distance
    https://en.wikipedia.org/wiki/Great-circle_distance
    """

    latitude1, longitude1 = point1
    latitude2, longitude2 = point2

    latitude1 = math.pi*latitude1 / 180
    latitude2 = math.pi*latitude2 / 180

    d_longitude = math.radians(math.fabs(longitude1 - longitude2))
    d_latitude = math.fabs(latitude1 - latitude2)

    a = math.sin(d_latitude/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(d_longitude/2)**2
    d_sigma = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return d_sigma * EARTH_RADIUS
