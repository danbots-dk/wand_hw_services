#!/bin/python3
from MAX17048 import BatteryService
from MCP23008 import IOexpander
import board
import json
import time 
import os
import datetime
import posix
import errno

i2c = board.I2C()
ioService = IOexpander(i2c)
batteryService = BatteryService(i2c)
WRITE_PIPE_NAME = "/tmp/battery_stats"
delay_s = 60
start_latch = 1
if not os.path.exists(WRITE_PIPE_NAME):
    os.mkfifo(WRITE_PIPE_NAME)
oldTime = time.time()

# Path to the lock file
lock_file = "/var/run/i2c_lock"
# Create the lock file
if os.path.isfile(lock_file): 
    lock = open(lock_file, "r+")
else:
    with open(lock_file, "w") as f:
        f.write("")

while(1):

    
    if (time.time()-oldTime >= delay_s or start_latch == 1):
        # Obtain i2c lock
        lock = open(lock_file, "r+")
        fcntl.flock(lock, fcntl.LOCK_EX)
        batState = batteryService.writeStats()

        batState["isCharging"] = ioService.isCharging()
        batState["isBattery"] = ioService.isBattery()
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()
        try:
            # NONBLOCK uses more cpu but is up to date
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            #fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY)
            batState = json.dumps(batState, indent=4)
            posix.write(fifo_fd, batState.encode())
            posix.close(fifo_fd)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        oldTime = time.time()
        start_latch = 0

