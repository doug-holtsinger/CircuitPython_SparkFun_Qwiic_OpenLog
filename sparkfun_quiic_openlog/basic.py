# SPDX-FileCopyrightText: 2017 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""

"""
from micropython import const
from sparkfun_quiic_openlog.protocol import I2C_Impl
from busio import I2C
from digitalio import DigitalInOut
from time import sleep

__version__ = "0.0.1"
__repo__ = "https://github.com/doug-holtsinger/CircuitPython_SparkFun_Qwiic_OpenLog"

#    I2C ADDRESS/BITS/SETTINGS
#    -----------------------------------------------------------------------

""" Default I2C address """
_QOL_DEFAULT_ADDRESS         = const(0x2A)
""" I2C Register Addresses"""
_QOL_STATUS_REG              = const(0x01)
_QOL_FW_MSB_REG              = const(0x02)
_QOL_FW_LSB_REG              = const(0x03)
_QOL_INT_ENABLE_REG          = const(0x04)
_QOL_INITIALIZE_REG          = const(0x05)
_QOL_CREATE_FILE_REG         = const(0x06)
_QOL_MAKE_DIRECTORY_REG      = const(0x07)
_QOL_CHANGE_DIRECTORY_REG    = const(0x08)
_QOL_READ_FILE_REG           = const(0x09)
_QOL_START_POSITION_REG      = const(0x0A)
_QOL_APPEND_FILE_REG         = const(0x0B)
_QOL_WRITE_FILE_REG          = const(0x0C)
_QOL_FILE_SIZE_REG           = const(0x0D)
_QOL_LIST_REG                = const(0x0E)
_QOL_REMOVE_REG              = const(0x0F)
_QOL_REMOVE_RECURSIVELY_REG  = const(0x10)
_QOL_SYNC_FILE_REG           = const(0x11)
_QOL_I2C_ADDRESS_REG         = const(0x1E)

_QOL_STATUS_SD_INIT_GOOD         = const(0)
_QOL_STATUS_LAST_COMMAND_SUCCESS = const(1)
_QOL_STATUS_LAST_COMMAND_KNOWN   = const(2)

class Sparkfun_Qwiic_OpenLog:
    """
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, bus_implementation) -> None:
        """
        """
        self._bus_implementation = bus_implementation
        sleep(0.05)   # Wait for board to respond to I2C 
        init_good = self._wait_init_good()

    def _initialize(self) -> bool:
        """Initialize the QOL"""
        self._write_register_byte(_QOL_INITIALIZE_REG, 0x00)
        return self._wait_cmd_success()

    def _wait_init_good(self) -> bool:
        ready = False
        cnt = 10
        while cnt < 10:
            ready = self.get_status() & (1 << _QOL_STATUS_SD_INIT_GOOD)
            if ready: 
                break
            sleep(0.05)
            cnt = cnt + 1
        return ready

    def _wait_cmd_success(self) -> bool:
        ready = 0
        cnt = 10
        while cnt < 10:
            ready = self.get_status() & (1 << _QOL_STATUS_LAST_COMMAND_SUCCESS)
            if ready:
                break
            sleep(0.05)
            cnt = cnt + 1
        return ready

    def _read_byte(self, register: int) -> int:
        """Read a byte register value and return it"""
        return self._read_register(register, 1)[0]

    def _read_register(self, register: int, length: int) -> bytearray:
        return self._bus_implementation.read_register(register, length)

    def _write_register_byte(self, register: int, value: int) -> None:
        self._bus_implementation.write_register_byte(register, value)

    def get_status(self) -> int:
        """Get the value from the status register in the device"""
        return self._read_byte(_QOL_STATUS_REG)


class Sparkfun_Qwiic_OpenLog_I2C(Sparkfun_Qwiic_OpenLog):

    """Driver for Quiic OpenLog connected over I2C

    """

    def __init__(self, i2c: I2C, address: int = _QOL_DEFAULT_ADDRESS) -> None:
        super().__init__(I2C_Impl(i2c, address))


