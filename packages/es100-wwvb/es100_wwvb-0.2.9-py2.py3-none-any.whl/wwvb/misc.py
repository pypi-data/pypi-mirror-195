"""

    WWVB receiver

    All times are kept in UTC base (no local times used)

"""

import sys
from datetime import timedelta
from math import degrees, radians, sin, cos, acos, atan2

from .sun import Sun

WWVB_FT_COLLINS = [40.6777225, -105.047153, 1585]  # latitude, longitude, and MASL
MY_RECEIVER = [36.9812160, -122.026706, 60]  # Santa Cruz, California, USA

RADIOWAVE_SPEED = 299250.0              # km / sec

def caculate_latency():
    """ caculate_latency """

    distance_km = great_circle_km(
                    MY_RECEIVER[0], MY_RECEIVER[1],
                    WWVB_FT_COLLINS[0], WWVB_FT_COLLINS[1])

    bearing = bearing_degrees(
                    MY_RECEIVER[0], MY_RECEIVER[1],
                    WWVB_FT_COLLINS[0], WWVB_FT_COLLINS[1])

    latency_secs = distance_km / RADIOWAVE_SPEED
    print('The great circle distance to WWVB: %.1f Km and direction is %.1f degrees; hence latency %.3f Milliseconds' % (
                distance_km,
                bearing,
                latency_secs * 1000.0
            ),
            file=sys.stderr
        )
    return timedelta(microseconds=latency_secs*1000000.0)

sun_at_wwvb_ft_collins = Sun(WWVB_FT_COLLINS[0], WWVB_FT_COLLINS[1], WWVB_FT_COLLINS[2])
sun_at_my_receiver = Sun(MY_RECEIVER[0], MY_RECEIVER[1], MY_RECEIVER[2])

def is_it_nighttime(dtime=None):
    """ is_it_nighttime """

    # VLW Reception is better at night (you learned that when becoming a ham radio operator)

    # if both location are dark presently, then radio waves should flow
    return bool(sun_at_wwvb_ft_collins.civil_twilight(dtime) and sun_at_my_receiver.civil_twilight(dtime))

"""
    You can double check this via GCMAP website.

    http://www.gcmap.com/mapui?P=WWVB%3D40.678062N105.046688W%3B%0D%0ASJC-WWVB&R=1505Km%40WWVB&PM=b%3Adisc7%2B%22%25U%25+%28N%22&MS=wls2&DU=km

"""

def great_circle_km(lat1, lon1, lat2, lon2):
    """ great_circle """
    # https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 6371 * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))

def bearing_degrees(lat1, lon1, lat2, lon2):
    """ bearing_degrees """
    # https://stackoverflow.com/questions/54873868/python-calculate-bearing-between-two-lat-long
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    x = cos(lat2) * sin(lon2 - lon1)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)
    return degrees(atan2(x, y))
