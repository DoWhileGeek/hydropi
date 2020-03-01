#!/usr/bin/python

import sys

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, out_pump
from hydropi.config import config


def drain():
    print("turning on off_pump")
    out_pump.on()

    print("waiting for low_float")
    low_float.wait_for_release()

    out_pump.off()

    while True:
        low_float.wait_for_press(config["timeout"])
        if low_float.is_pressed:
            sleep(config["delay"])
            out_pump.on()
            low_float.wait_for_release()
            out_pump.off()
        else:
            break


def main_loop():
    drain()

    # turn all pumps off
    out_pump.off()

    sys.exit(0)


if __name__ == "__main__":
    main_loop()
