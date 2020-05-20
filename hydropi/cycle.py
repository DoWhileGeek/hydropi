#!/usr/bin/env python3

import argparse
import sys
from time import sleep
import logging
import datetime

import gpiozero
from gpiozero import Button

from hydropi.devices import low_float, high_float, in_pump, out_pump
from hydropi.config import config
from hydropi.utils.logging import setup_logging
from hydropi.utils.pid_lock import pid_lock


def fill(args):
    logging.info("turning on in_pump")
    pre_fill = datetime.datetime.utcnow()
    in_pump.on()

    high_float.wait_for_release(config["fill_timeout"])
    if high_float.is_pressed:
        logging.warning("fill timed out, cutting it short")

    logging.debug(
        f"seconds from empty to filled: {(datetime.datetime.utcnow() - pre_fill).total_seconds()}"
    )

    logging.info(f"overfilling for {config['overfill']} seconds")
    sleep(config["overfill"])

    in_pump.off()
    logging.debug(
        f"seconds from emmpty to overfilled: {(datetime.datetime.utcnow() - pre_fill).total_seconds()}"
    )


def drain(args):
    logging.info("turning on out_pump")
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
            logging.info("redraining")
            low_float.wait_for_press()
            sleep(config["overfill"])
            out_pump.off()


def cycle(args):
    fill(args)
    drain(args)


def ping(args):
    logging.info("pong!")


def main():
    setup_logging()

    try:
        # create the top-level parser
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        # create the parser for the "fill" command
        parser_fill = subparsers.add_parser("fill")
        parser_fill.set_defaults(func=fill)

        # create the parser for the "drain" command
        parser_drain = subparsers.add_parser("drain")
        parser_drain.set_defaults(func=drain)

        # create the parser for the "cycle" command
        parser_drain = subparsers.add_parser("cycle")
        parser_drain.set_defaults(func=cycle)

        # create the parser for the "drain:tank" command
        parser_drain = subparsers.add_parser("drain:tank")
        parser_drain.set_defaults(func=drain_tank)

        # create the parser for the "ping" command
        parser_drain = subparsers.add_parser("ping")
        parser_drain.set_defaults(func=ping)

        # parse the args and call whatever function was selected
        args = parser.parse_args()
        args.func(args)

    except KeyboardInterrupt:
        logging.info("cancelling")


# utilities
def drain_tank(args):
    logging.info("turning on out_pump")
    try:
        in_pump.on()

        while True:
            pass
    except KeyboardInterrupt:
        logging.info("shuting down")


if __name__ == "__main__":
    main()
