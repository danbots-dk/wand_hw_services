#!/bin/python3
from MAX17048 import BatteryService
from ioLib import IOexpander
import board
import json
import time 
import os
import datetime
import posix
import errno
import fcntl

# Initialize I2C and create instances of BatteryService and IOexpander
i2c = board.I2C()
ioService = IOexpander(i2c)
batteryService = BatteryService(i2c)

# Define the path for the named pipe (FIFO)
WRITE_PIPE_NAME = "/tmp/battery_stats"

# Define the delay interval for updating battery stats
delay_s = 5
start_latch = 1
oldTime = time.time()

# Create the named pipe if it doesn't exist
if not os.path.exists(WRITE_PIPE_NAME):
    os.mkfifo(WRITE_PIPE_NAME)

# Path to the lock file
lock_file = "/var/lock/i2c_lock"

# Create the lock file if it doesn't exist, or open it for reading and writing
if not os.path.isfile(lock_file):
    with open(lock_file, "w") as f:
        f.write("")
    f.close()

while True:
    if (time.time()-oldTime >= delay_s or start_latch == 1):
        # Obtain I2C lock
        lock = open(lock_file, "r+")
        fcntl.flock(lock, fcntl.LOCK_EX)

        # Retrieve battery statistics and additional IOexpander data
        batState = batteryService.writeStats()
        batState["isCharging"] = ioService.isCharging()
        batState["isBattery"] = ioService.isBattery()
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()

        try:
            # Write battery state to the named pipe (FIFO)
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            batState = json.dumps(batState, indent=4)
            posix.write(fifo_fd, batState.encode())
            posix.close(fifo_fd)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        oldTime = time.time()
        start_latch = 0
    time.sleep(0.1)
