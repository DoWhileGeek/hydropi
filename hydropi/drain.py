#!/usr/bin/python

import sys
from time import sleep

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, out_pump
from hydropi.config import config
from hydropi.cycle import drain


def main_loop():
    drain()

    # turn all pumps off
    out_pump.off()

    sys.exit(0)


if __name__ == "__main__":
    main_loop()
