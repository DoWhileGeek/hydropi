#!/usr/bin/python

import sys
from time import sleep

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, high_float, in_pump, out_pump
from hydropi.config import config


def setup():
    if not low_float.is_pressed or not high_float.is_pressed:
        print("the floats are in a strange state, quitting")
        raise Exception("bad start state")


def fill():
    print("turning on in_pump")
    while True:
        high_float.wait_for_press(config["timeout"])
        if high_float.is_pressed:
            break
        else:
            sleep(config["delay"])
            in_pump.on()
            print("refilling")
            high_float.wait_for_release()
            sleep(config["overfill"] * 2)
            in_pump.off()



def drain():
    print("turning on out_pump")
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
    setup()
    fill()
    drain()

    # turn all pumps off
    in_pump.off()
    out_pump.off()

    sys.exit(0)


if __name__ == "__main__":
    main_loop()
