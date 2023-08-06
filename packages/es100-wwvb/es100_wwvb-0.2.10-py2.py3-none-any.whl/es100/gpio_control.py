"""
    GPIO control (for EN & IRQ lines)
"""

import sys

try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

IRQ_DELAY_SEC = 0.1                         # 100ms: module version 1 only

class ES100GPIOError(Exception):
    """ ES100GPIOError """

class ES100GPIO:
    """ ES100GPIO """

    def __init__(self, en, irq, debug=False):
        """ __init__ """
        if not GPIO:
            raise ES100GPIOError('RPi.GPIO package not installed - are you actually running on a Raspberry Pi?')
        self._gpio_en = en
        self._gpio_irq = irq
        self._debug = debug
        self._setup()

    def _setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._gpio_en, GPIO.OUT)
        GPIO.setup(self._gpio_irq, GPIO.IN, GPIO.PUD_DOWN)

    def __del__(self):
        """ __del__ """
        if not GPIO:
            return
        self._close()

    def _close(self):
        """ _close """
        self.en_low()
        GPIO.cleanup()

    def en_low(self):
        """ en_low """
        # Enable Input. When low, the ES100 powers down all circuitry.
        GPIO.output(self._gpio_en, GPIO.LOW)

    def en_high(self):
        """ en_high """
        # Enable Input. When high, the device is operational.
        GPIO.output(self._gpio_en, GPIO.HIGH)

    def irq_wait(self):
        """ irq_wait """
        # Interrupt Output. Active low to signal data available to an external controller.
        if self._debug:
            sys.stderr.write('IRQ WAIT: ')
            sys.stderr.flush()
        while GPIO.input(self._gpio_irq):
            if self._debug:
                sys.stderr.write('H')
                sys.stderr.flush()
            # now wait (for any transition) - way better than looping, sleeping, and checking
            channel = GPIO.wait_for_edge(self._gpio_irq, GPIO.BOTH, timeout=10*1000)
            if channel is None:
                if self._debug:
                    sys.stderr.write('.')
                    sys.stderr.flush()
        if self._debug:
            sys.stderr.write(' L\n')
            sys.stderr.flush()
