from math import radians, cos, sin, asin, sqrt


def haversine(from_lat, from_lon, to_lat, to_lon):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    from_lon, from_lat, to_lon, to_lat = map(radians, [from_lon, from_lat, to_lon, to_lat])

    # haversine formula
    dlon = to_lon - from_lon
    dlat = to_lat - from_lat
    a = sin(dlat / 2) ** 2 + cos(from_lat) * cos(to_lat) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r
