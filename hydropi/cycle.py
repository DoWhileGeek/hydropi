#!/usr/bin/python

import sys
from time import sleep

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, high_float, in_pump, out_pump
from hydropi.config import config


def fill():
    print("turning on in_pump")
    in_pump.on()

    high_float.wait_for_release()

    print(f"overfilling for {config['overfill']} seconds")
    sleep(config["overfill"])

    in_pump.off()



def drain():
    print("turning on out_pump")
    out_pump.on()
    low_float.wait_for_press()
    out_pump.off()

    while True:
        low_float.wait_for_release(config["timeout"])
        if low_float.is_pressed:
            break
        else:
            sleep(config["delay"])
            out_pump.on()
            print("redraining")
            low_float.wait_for_press()
            sleep(config["overfill"])
            out_pump.off()


def main_loop():
    fill()
    drain()

    # turn all pumps off
    in_pump.off()
    out_pump.off()

    sys.exit(0)


if __name__ == "__main__":
    main_loop()
