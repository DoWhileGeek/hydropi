#!/usr/bin/python

import sys
from time import sleep

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, high_float, in_pump, out_pump
from hydropi.config import config


def setup():
    if low_float.is_pressed or high_float.is_pressed:
        print("the floats are in a strange state, quitting")
        raise Exception("bad start state")


def fill():
    print("turning on in_pump")
    in_pump.on()


    print("waiting for high_float")
    high_float.wait_for_press()

    print("overfilling")
    sleep(config["overfill"])

    print("turning off in_pump")
    in_pump.off()

    while True:
        high_float.wait_for_release(config["timeout"])
        if not high_float.is_pressed:
            sleep(config["delay"])
            in_pump.on()
            print("refilling")
            high_float.wait_for_press()
            sleep(config["overfill"])
            in_pump.off()
        else:
            break



def drain():
    print("turning on off_pump")
    out_pump.on()

    print("waiting for low_float")
    low_float.wait_for_release()

    out_pump.off()

    while True:
        low_float.wait_for_release(config["timeout"])
        if not low_float.is_pressed:
            sleep(config["delay"])
            out_pump.on()
            print("redraining")
            low_float.wait_for_release()
            out_pump.off()
        else:
            break


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
