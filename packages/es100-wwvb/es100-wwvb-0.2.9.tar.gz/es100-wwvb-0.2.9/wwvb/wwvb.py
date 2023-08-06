#!/usr/bin/env python3

"""

    WWVB receiver

    All times are UTC base

WWVB Location ...

    WWVB
    5701 CO-1,
    Fort Collins, CO 80524
    https://goo.gl/maps/KgRn1jDmJ3zSUfxx7

    40.678062N, 105.046688W

    https://www.nist.gov/pml/time-and-frequency-division/time-distribution/radio-station-wwvb

    North antenna coordinates: 40° 40' 51.3" N, 105° 03' 00.0" W == 40.680917 N, 105.050000 W
    South antenna coordinates: 40° 40' 28.3" N, 105° 02' 39.5" W == 40.674528 N, 105.044306 W

Speed of radio waves ...

    https://ieeexplore.ieee.org/document/1701081

    299,775 km/s in a vacuum
    299,250 km/s for 100Khz at ground level
    299,690 km/s for cm waves
    299,750 km/s for aircraft at 30,000 feet (9,800 meters)

    I choose 299,250 km/s

"""

import sys
import time
import logging
from datetime import datetime, timezone

from es100 import ES100, ES100Error
from .misc import caculate_latency, is_it_nighttime

# ES100's pins as connected to R.Pi GPIO pins

                                        # ES100 Pin 1 == GND
GPIO_EN   = 7  # GPIO-4                 # ES100 Pin 2 == EN Enable
                                        # ES100 Pin 3 == SDA
                                        # ES100 Pin 4 == SCL
GPIO_IRQ  = 11 # GPIO-17                # ES100 Pin 5 == IRQ Interupt Request
                                        # ES100 Pin 6 == VCC 3.6V (2.0-3.6V recommended)

def doit(program_name, args):
    """ doit """

    # needed within other modules
    required_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(format=required_format)

    latency = caculate_latency()

    try:
        es100 = ES100(en=GPIO_EN, irq=GPIO_IRQ, debug=True)
    except ES100Error as err:
        sys.exit(err)

    while True:
        nighttime = is_it_nighttime()
        nighttime = True # XXX for testing
        try:
            if nighttime:
                received_dt = es100.time(tracking=False)
            else:
                received_dt = es100.time(tracking=True)
        except (ES100Error, OSError) as err:
            #sys.exit(err)
            received_dt = None
            time.sleep(0.5)
        if received_dt:
            # by default WWVB has microsecond == 0 (as it's not in the receive frames)
            received_dt += latency
            now = datetime.utcnow()
            now = now.replace(tzinfo=timezone.utc)
            print('WWVB: %s at %s' % (received_dt, now))
            sys.stdout.flush()

def wwvb(args=None):
    """ wwvb """

    if args is None:
        args = sys.argv[1:]

    try:
        doit(sys.argv[0], args)
    except KeyboardInterrupt:
        sys.exit('^C')

    sys.exit(0)
