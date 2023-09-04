#/bin/python3
from __future__ import annotations

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice


class TMP1075:
    TEMP_REGISTER = bytearray([0x00])
    CONFIG_REGISTER = bytearray([0x01])

    def __init__(self, address: int = 0x4F):
        comm_port = busio.I2C(board.SCL, board.SDA)
        self.i2c = I2CDevice(comm_port, address)

    def get_temperature(self) -> float:
        b = bytearray(2)
        self.i2c.write_then_readinto(self.TEMP_REGISTER, b)
        return ((b[0] << 4) + (b[1] >> 4)) * 0.0625
