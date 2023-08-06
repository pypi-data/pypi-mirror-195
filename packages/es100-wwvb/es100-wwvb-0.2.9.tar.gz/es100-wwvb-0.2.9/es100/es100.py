"""

Description ...

    WWVB parser on i2c bus for ES100

Copyright ...

    Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin
    Copyright (C) 2023 @mahtin

References ...

    https://universal-solder.ca/downloads/EverSet_ES100-MOD_V1.1.pdf
    https://sites.google.com/site/wwvbreceiverwitharduino/home/es100_starter_code_with_amendments?authuser=0
    https://github.com/fiorenzo1963/es100-wwvb-refclock

    curl -O https://universal-solder.ca/downloads/wwvb_bpsk_es100.zip

    https://www.nist.gov/pml/time-and-frequency-division/time-distribution/radio-station-wwvb
    https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=914904

Additional software ...

    https://github.com/fiorenzo1963/es100-wwvb-refclock/blob/master/es100_wwvb.py

Hardware ...

    https://universal-solder.ca/product/everset-es100-wwvb-starter-kit/
    https://universal-solder.ca/product/everset-es100-mod-wwvb-bpsk-phase-modulation-receiver-module/
    https://universal-solder.ca/product/canaduino-application-development-kit-with-everset-es100-mod-wwvb-bpsk-atomic-clock-receiver-module/

"""

import time
from datetime import datetime, timezone
import logging
from enum import IntEnum
import random

from .gpio_control import ES100GPIO, ES100GPIOError
from .i2c_control import ES100I2C, ES100I2CError

class ES100Error(Exception):
    """ raise this any ES100 error """

class ES100:
    """ ES100 """

    I2C_DEFAULT_BUS = 1
    ES100_SLAVE_ADDR = 0x32             # I2C slave address

    ENABLE_DELAY_SEC = 0.1              # 100ms: module version 1 only

    # ES100 SERIAL INTERFACE REGISTER MAP
    class REG(IntEnum):
        """ REG """

        CONTROL0        = 0x00
        CONTROL1        = 0x01
        IRQSTATUS       = 0x02
        STATUS0         = 0x03
        YEAR            = 0x04
        MONTH           = 0x05
        DAY             = 0x06
        HOUR            = 0x07
        MINUTE          = 0x08
        SECOND          = 0x09
        NEXT_DST_MONTH  = 0x0a
        NEXT_DST_DAY    = 0x0b
        NEXT_DST_HOUR   = 0x0c
        DEVICE_ID       = 0x0d   # should return 0x10 (the device id of ES100)
        RESERVED0       = 0x0e
        RESERVED1       = 0x0f

    # Control0 Read/Write
    class CONTROL0(IntEnum):
        """ CONTROL0 """
        START           = 0x01  # 1 == start processing, 0 == stops/stopped receiving
        ANT1OFF         = 0x02  # 1 == Antenna1 disabled, 0 == Antenna1 enabled
        ANT2OFF         = 0x04  # 1 == Antenna2 disabled, 0 == Antenna2 enabled
        STARTANT        = 0x08  # 1 == Start reception with Antenna2, 0 = Antenna1
        TRACKINGENABLE  = 0x10  # 1 == Tracking mode enabled, 0 == disabled
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

        # Valid values are:
        # 0x01 normal mode, starts on Antenna1, toggles between antennas
        # 0x03 (Antenna 2 only)
        # 0x05 (Antenna 1 Only)
        # 0x09 normal mode, starts on Antenna2, toggles between antennas
        # 0x13 tracking mode, Antenna2
        # 0x15 tracking mode, Antenna1

    # Control1 Read/Write (presently unused)
    class CONTROL1(IntEnum):
        """ CONTROL1 """
        BIT0            = 0x01
        BIT1            = 0x02
        BIT2            = 0x04
        BIT3            = 0x08
        BIT4            = 0x10
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

    # IRQ Status Read only
    class IRQSTATUS(IntEnum):
        """ IRQSTATUS """
        RX_COMPLETE     = 0x01 # 1 == Reception complete, 0 == (default)
        BIT1            = 0x02
        CYCLE_COMPLETE  = 0x04 # 1 == Cycle Complete, unsuccessful reception, 0 == (default)
        BIT3            = 0x08
        BIT4            = 0x10
        BIT5            = 0x20
        BIT6            = 0x40
        BIT7            = 0x80

    # Status0 Read Only
    class STATUS0(IntEnum):
        """ STATUS0 """
        RX_OK           = 0x01  # 1 == successful reception
        ANT             = 0x02  # 1 == Antenna2, 0 == Antenna1
        BIT2            = 0x04
        LSW0            = 0x08  # LSW[0:1] 00 == Current month doesn't have leap second
        LSW1            = 0x10  # LSW[0:1] 10 == Negative leap second, 11 == positive leap second
        DST0            = 0x20  # DST[0:1] 00 == No DST, 10 == DST begins today
        DST1            = 0x40  # DST[0:1] 11 == DST in effect, 01 == DST ends today
        TRACKING        = 0x80  # 1 == reception was tracking operation

    def __init__(self, en=None, irq=None, bus=None, address=None, debug=False):
        """ __init """

        self._log = logging.getLogger(__class__.__name__)
        self._debug = debug
        if self._debug:
            self._log.setLevel(logging.DEBUG)

        self._gpio_en = en
        if not self._gpio_en:
            raise ES100Error('gpio en (enable) pin must be provided')

        self._gpio_irq = irq
        if not self._gpio_irq:
            raise ES100Error('gpio irq (interupt-request) pin must be provided')

        self._i2c_bus = bus
        if self._i2c_bus is not None:
            if self._i2c_bus < 0 or self._i2c_bus > 999:
                raise ES100Error('i2c bus number error: %s' % bus)
        else:
            self._i2c_bus = ES100.I2C_DEFAULT_BUS

        self._i2c_address = address
        if self._i2c_address is not None:
            if self._i2c_address < 0 or self._i2c_address > 127:
                raise ES100Error('i2c address number error: %s' % address)
        else:
            self._i2c_address = ES100.ES100_SLAVE_ADDR

        # start settting up hardware - if it exists!

        self._gpio = None
        self._i2c = None

        try:
            self._gpio = ES100GPIO(self._gpio_en, self._gpio_irq, debug=debug)
        except ES100GPIOError as err:
            raise ES100Error('GPIO open error: %s' % (err)) from err
        self._log.info('gpio connected (EN/Enable=%d IRQ=%d)', self._gpio_en, self._gpio_irq)

        try:
            self._i2c = ES100I2C(self._i2c_bus, self._i2c_address, debug=debug)
        except ES100I2CError as err:
            raise ES100Error('i2c bus %d open error: %s' % (self._i2c_bus, err)) from err
        self._log.info('i2c connected (bus=%d address=0x%02x)', self._i2c_bus, self._i2c_address)

        self._device_id = None
        self._recv_date = {}
        self._recv_time = {}
        self._recv_dst_info = {}
        self.begin_time = datetime.utcnow()
        self.end_time = None
        self.elapsed_time = None
        self._status0 = 0x00
        self._irq_status = 0x00

        # find device id
        self._enable()
        time.sleep(ES100.ENABLE_DELAY_SEC)
        if not self.es100_device_id():
            raise ES100Error('i2c bus probe failed to find ES100 chip')

        # self._disable()

    def __del__(self):
        """ __del__ """

        if self._i2c:
            self._i2c = None
            self._log.info('i2c disconnected')
        if self._gpio:
            self._gpio = None
            self._log.info('gpio disconnected')

    def _enable(self):
        """ _enable """
        self._gpio.en_high()
        self._log.info('enable set high')

    def _disable(self):
        """ _disable """
        self._gpio.en_low()
        self._log.info('enable set low')

    def _irq_wait(self):
        """ _irq_wait """
        self._log.info('wait for irq')
        self._gpio.irq_wait()

    def read_register(self, addr):
        """ read_register """
        try:
            self._i2c.write(addr)
        except ES100I2CError as err:
            self._log.error('i2c read: %s', err)
            raise ES100Error('i2c read: %s' % (err)) from err

        try:
            rval = self._i2c.read()
        except ES100I2CError as err:
            self._log.error('i2c read: %s', err)
            raise ES100Error('i2c read: %s' % (err)) from err
        self._log.info('register %d read => 0x%02x', addr, rval & 0xff)
        return rval & 0xff

    def write_register(self, addr, data):
        """ write_register """
        self._log.info('register %d write <= 0x%02x', addr, data)
        try:
            self._i2c.write_addr(addr, data)
        except ES100I2CError as err:
            self._log.error('i2c write: %s', err)
            raise ES100Error('i2c write: %s' % (err)) from err

    def _get_device_id(self):
        """ _get_device_id """
        self._log.info('get device_id')
        #Read DEVICE_ID register
        return self.read_register(int(ES100.REG.DEVICE_ID))

    def _get_irq_status(self):
        """ _get_irq_status """
        self._log.info('get irq')
        #Read IRQ status register
        return self.read_register(int(ES100.REG.IRQSTATUS))

    def _get_status0(self):
        """ _get_status0 """
        self._log.info('get status0')
        #Read STATUS0 register
        return self.read_register(int(ES100.REG.STATUS0))

    def start_rx(self, antenna=1, tracking=False):
        """ start_rx """
        if antenna not in [1, 2]:
            raise ES100Error('antenna number incorrect: %d' % (antenna))
        if not tracking:
            self._log.info('start rx via Antenna%d', antenna)
            if antenna == 1:
                self.write_register(int(ES100.REG.CONTROL0),
                                        ES100.CONTROL0.START)
            else:
                self.write_register(int(ES100.REG.CONTROL0),
                                        ES100.CONTROL0.START | ES100.CONTROL0.STARTANT)
        else:
            self._log.info('start tracking via Antenna%d', antenna)
            if antenna == 1:
                self.write_register(int(ES100.REG.CONTROL0),
                                        ES100.CONTROL0.START | ES100.CONTROL0.TRACKINGENABLE | ES100.CONTROL0.ANT2OFF)
            else:
                self.write_register(int(ES100.REG.CONTROL0),
                                        ES100.CONTROL0.START | ES100.CONTROL0.TRACKINGENABLE | ES100.CONTROL0.ANT1OFF)
        # perform read of control0 register for i2c debug only
        rval = self.read_register(int(ES100.REG.CONTROL0))
        return rval

    def start_tracking(self, antenna=1):
        """ start_tracking """

        # The duration of a tracking reception is ~24.5 seconds (22 seconds of reception,
        # plus ~2.5 seconds of processing and IRQ- generation),

        # The write to Control 0 must occur when the clock second transitions to :55
        # (refer to the timing diagrams to see how this supports drift between +4s and -4s).

        return self.start_rx(antenna=antenna, tracking=True)

    def read_recv_info_registers(self):
        """ read_recv_info_registers """
        self._log.info('read recv info registers')
        self._recv_date = {}
        self._recv_time = {}
        self._recv_dst_info = {}
        for reg in [ES100.REG.YEAR, ES100.REG.MONTH, ES100.REG.DAY]:
            self._recv_date[reg.name] = self.read_register(int(reg.value))
        for reg in [ES100.REG.HOUR, ES100.REG.MINUTE, ES100.REG.SECOND]:
            self._recv_time[reg.name] = self.read_register(int(reg.value))
        for reg in [ES100.REG.NEXT_DST_MONTH, ES100.REG.NEXT_DST_DAY, ES100.REG.NEXT_DST_HOUR]:
            self._recv_dst_info[reg.name] = self.read_register(int(reg.value))
        if self._debug:
            self._log.debug('recv date = %s', (self._recv_date))
            self._log.debug('recv time = %s', (self._recv_time))
            self._log.debug('recv dst info = %s', (self._recv_dst_info))

    @classmethod
    def _bcd(cls, val):
        """ _bcd """
        return (val & 0x0f) + ((val >> 4) & 0x0f) * 10

    def es100_device_id(self):
        """ es100_device_id """

        if self._device_id is None:
            try:
                self._device_id = self._get_device_id()
            except ES100Error as err:
                self._device_id = 0x00

        if self._device_id == 0x10:
            self._log.info('device ID = 0x%02x (confirmed ES100)', self._device_id)
            return True
        else:
            self._log.info('device ID = 0x%02x (unknown device)', self._device_id)
            return False

    def wait_till_55seconds(self):
        """ wait_till_55seconds """

        # Tracking should not start till :55 second point
        # (we assume ntp is running - chicken-n-egg issue)

        time_now = datetime.utcnow()
        remaining_seconds = 55.0 - (time_now.second + time_now.microsecond/1000000.0)
        if remaining_seconds < 0.0:
            remaining_seconds += 60.0
        self._log.info('sleeping %.3f seconds till :55 point', remaining_seconds)
        time.sleep(remaining_seconds)

    def es100_receive(self, antenna=None, tracking=False):
        """ es100_receive """

        # initialize gpio's
        # self._disable()
        time.sleep(ES100.ENABLE_DELAY_SEC)

        # enable and delay
        self._enable()
        time.sleep(ES100.ENABLE_DELAY_SEC)
        # start reception
        if not antenna:
            antenna = random.choice([1, 2])
        if not tracking:
            self.start_rx(antenna)
        else:
            self.wait_till_55seconds()
            self.start_tracking(antenna)

        # loop until time received
        self._irq_status = 0x00
        self._status0 = 0x00
        system_receive_time = None

        # We wait ~134 seconds for a 1-minute frame reception.
        while True:
            # read interrupt status and status0
            self._irq_status = self._get_irq_status()
            self._status0 = self._get_status0()

            status_ok = bool(self._status0 & ES100.STATUS0.RX_OK)
            rx_antenna =  2 if self._status0 & ES100.STATUS0.ANT else 1
            tracking_operation = bool(self._status0 & ES100.STATUS0.TRACKING)

            self._log.info('irq_status = 0x%02x <-,-,-,-,-,%s,-,%s> | status0 = 0x%02x <%s,...,%s,-,%s>',
                                self._irq_status,
                                'CYCLE_COMPLETE' if self._irq_status & ES100.IRQSTATUS.CYCLE_COMPLETE else '-',
                                'RX_COMPLETE' if self._irq_status & ES100.IRQSTATUS.RX_COMPLETE else '-',
                                self._status0,
                                'TRACKING' if tracking_operation else '-',
                                'Antenna' + str(rx_antenna),
                                'RX_OK' if status_ok else '-',
                        )

            if (self._irq_status & ES100.IRQSTATUS.RX_COMPLETE) != 0x00:
                # save away the current time - i.e. time of decoded reception
                system_receive_time = datetime.utcnow()
                system_receive_time = system_receive_time.replace(tzinfo=timezone.utc)
                # go do stuff!
                break

            # now we wait - how long? 134 seconds according to the manual
            # we don't actually read the IRQ line
            # we look for an edge (up or down) - way more cpu efficient!
            self._irq_wait()

        self.read_recv_info_registers()

        # self._disable()

        # return timer value when interrupt occurred
        return system_receive_time

    def caculate_date_time(self):
        """ caculate_date_time """

        lsw0 = self._status0 & ES100.STATUS0.LSW0
        lsw1 = self._status0 & ES100.STATUS0.LSW1

        dst0 = self._status0 & ES100.STATUS0.DST0
        dst1 = self._status0 & ES100.STATUS0.DST1

        if lsw0:
            self._log.info('%s leap second', 'positive' if lsw1 else 'negative')

        if dst0:
            if dst1:
                self._log.info('DST in effect')
            else:
                self._log.info('DST begins today')
        else:
            if dst1:
                self._log.info('DST ends today')
            else:
                self._log.info('No DST')

        decimal_minutes = float(ES100._bcd(self._recv_time['MINUTE']))
        decimal_minutes += float(ES100._bcd(self._recv_time['SECOND']))/60.0
        self._log.info('minutes ... %s', decimal_minutes)

        # display next DST transition date
        self._log.info('Next DST transition = month %02d day %02d hour %02d DST status = 0x%1x',
                            ES100._bcd(self._recv_dst_info['NEXT_DST_MONTH'] & 0x1f),
                            ES100._bcd(self._recv_dst_info['NEXT_DST_DAY'] & 0x3f),
                            ES100._bcd(self._recv_dst_info['NEXT_DST_HOUR'] & 0x0f),
                            self._recv_dst_info['NEXT_DST_HOUR'] & 0xf0 >> 4
                        )

        self.end_time = datetime.utcnow()
        self.elapsed_time = self.end_time - self.begin_time
        self._log.info('Elapsed time to here... %s', self.elapsed_time)

        received_dt = datetime(
                                ES100._bcd(self._recv_date['YEAR'] & 0xff) + 2000,
                                ES100._bcd(self._recv_date['MONTH'] & 0x1f),
                                ES100._bcd(self._recv_date['DAY'] & 0x3f),
                                ES100._bcd(self._recv_time['HOUR'] & 0x3f),
                                ES100._bcd(self._recv_time['MINUTE'] & 0x7f),
                                ES100._bcd(self._recv_time['SECOND'] & 0x3f),
                                microsecond=0,
                                tzinfo=timezone.utc
                        )

        return received_dt

    def time(self, antenna=None, tracking=False):
        """ time """

        self.begin_time = datetime.utcnow()
        self.end_time = datetime.utcnow()
        self.elapsed_time = self.end_time - self.begin_time
        self._log.info('Elapsed time to here... %s', self.elapsed_time)

        try:
            # receive time from WWVB
            system_receive_time = self.es100_receive(antenna, tracking)
        except ES100Error as err:
            self._log.warning('read/receive failed: %s', err)
            return None

        self.end_time = datetime.utcnow()
        self.elapsed_time = self.end_time - self.begin_time
        self._log.info('Elapsed time to here... %s', self.elapsed_time)

        # display status register
        self._log.info('Status register = 0x%02x', self._status0)

        status_ok = bool(self._status0 & ES100.STATUS0.RX_OK)
        rx_antenna =  2 if self._status0 & ES100.STATUS0.ANT else 1

        if self._status0 & ES100.STATUS0.TRACKING:
            if status_ok:
                self._log.info('tracking operation successful, Antenna%d', rx_antenna)
            else:
                self._log.warning('tracking operation unsuccessful, Antenna%d', rx_antenna)
            # No value for date/time in tracking mode
            return None
        else:
            if status_ok:
                # this is where we go do a lot more work - we have a date/time received!
                self._log.info('reception successful, Antenna%d', rx_antenna)
            else:
                self._log.warning('reception unsuccessful, Antenna%d', rx_antenna)
                # No value for data/time, didn't get reception
                return None

        self._log.info('hh:mm:00 boundary occurred at system time =  %s', system_receive_time)
        return self.caculate_date_time()
