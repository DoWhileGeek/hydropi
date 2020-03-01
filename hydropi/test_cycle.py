import pytest
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

Device.pin_factory = MockFactory()

from .cycle import setup
from ..config import config



class TestStartState:
    def test_happy_path(self):
        setup()

    def test_low_float_triggered(self):
        low_float_pin = Device.pin_factory.pin(config['low_float'])

        low_float_pin.drive_low()
        with pytest.raises(Exception):
            setup()

    def test_high_float_triggered(self):
        low_float_pin = Device.pin_factory.pin(config['high_float'])

        low_float_pin.drive_low()
        with pytest.raises(Exception):
            setup()
