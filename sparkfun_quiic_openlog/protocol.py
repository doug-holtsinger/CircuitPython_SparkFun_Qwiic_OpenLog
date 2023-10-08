# SPDX-FileCopyrightText: 2022 Randall Bohn (dexter)
#
# SPDX-License-Identifier: MIT
"Provides the protocol objects for I2C and SPI"

from busio import I2C, SPI
from digitalio import DigitalInOut


class I2C_Impl:
    "Protocol implementation for the I2C bus."

    def __init__(self, i2c: I2C, address: int) -> None:
        from adafruit_bus_device import (  # pylint: disable=import-outside-toplevel
            i2c_device,
        )

        self._i2c = i2c_device.I2CDevice(i2c, address)

    def read_register(self, register: int, length: int) -> bytearray:
        "Read from the device register."
        with self._i2c as i2c:
            i2c.write(bytes([register & 0xFF]))
            result = bytearray(length)
            i2c.readinto(result)
            return result

    def write_register_byte(self, register: int, value: int) -> None:
        """Write to the device register"""
        with self._i2c as i2c:
            i2c.write(bytes([register & 0xFF, value & 0xFF]))


