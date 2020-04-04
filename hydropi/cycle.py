#!/usr/bin/env python3

import argparse
import sys
from time import sleep

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, high_float, in_pump, out_pump
from hydropi.config import config


def fill(args):
    print("turning on in_pump")
    in_pump.on()

    high_float.wait_for_release()

    print(f"overfilling for {config['overfill']} seconds")
    sleep(config["overfill"])

    in_pump.off()


def drain(args):
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


def cycle(args):
    fill(args)
    drain(args)


def main():
    try:
        # create the top-level parser
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        # create the parser for the "fill" command
        parser_fill = subparsers.add_parser('fill')
        parser_fill.set_defaults(func=fill)

        # create the parser for the "drain" command
        parser_drain = subparsers.add_parser('drain')
        parser_drain.set_defaults(func=drain)

        # create the parser for the "cycle" command
        parser_drain = subparsers.add_parser('cycle')
        parser_drain.set_defaults(func=cycle)

        # create the parser for the "drain:tank" command
        parser_drain = subparsers.add_parser('drain:tank')
        parser_drain.set_defaults(func=drain_tank)

        # parse the args and call whatever function was selected
        args = parser.parse_args()
        args.func(args)

    except KeyboardInterrupt:
        print("cancelling")


# utilities
def drain_tank(args):
    print("turning on out_pump")
    try:
        in_pump.on()
    except KeyboardInterrupt:
        print("shuting down")


if __name__ == "__main__":
    main()
