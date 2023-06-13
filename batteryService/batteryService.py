#!/bin/python3
from MAX17048 import BatteryService
from MCP23008 import IOexpander
import board
import json
import time 
import os
import datetime


i2c = board.I2C()
ioService = IOexpander(i2c)
batteryService = BatteryService(i2c)
bat_stats = "/tmp/battery_stats"
if not os.path.exists(bat_stats):
    os.mkfifo(bat_stats)

while(1):
    batState = batteryService.writeStats()

    batState["isCharging"] = ioService.isCharging()
    batState["isBattery"] = ioService.isBattery()

    bat_info = json.dumps(batState, indent=4)
    fifo = open(bat_stats, "w")
    fifo.write(bat_info)
    fifo.flush()
    fifo.close()