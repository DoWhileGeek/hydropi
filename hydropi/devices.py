import gpiozero
from gpiozero import Button

from hydropi.config import config

in_pump = gpiozero.OutputDevice(config["in_pump"], initial_value=False)
out_pump = gpiozero.OutputDevice(config["out_pump"], initial_value=False)

low_float = Button(config["low_float"])
high_float = Button(config["high_float"])
