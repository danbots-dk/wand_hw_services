#!/bin/python3
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import board
import json
import time 
import os
import datetime
import posix
import errno
import fcntl

# Initialize the I2C and LSM6DS3 sensor
i2c = board.I2C()
sox = LSM6DS3(i2c)

# Define the path for the named pipe (FIFO)
WRITE_PIPE_NAME = "/tmp/imu_stats"

# Define the delay and latch variables
delay_s = 0.1
start_latch = 1
oldTime = time.time()

# Create the named pipe if it doesn't exist
if not os.path.exists(WRITE_PIPE_NAME):
    os.mkfifo(WRITE_PIPE_NAME)

# Path to the lock file
lock_file = "/var/lock/i2c_lock"

# Create the lock file if it doesn't exist, or open it for reading and writing
if not(os.path.isfile(lock_file)):
    with open(lock_file, "w") as f:
        f.write("")
    f.close()

while True:
    if (time.time() - oldTime >= delay_s or start_latch == 1):
        try:
            # Obtain the I2C lock
            lock = open(lock_file, "r+")
            fcntl.flock(lock, fcntl.LOCK_EX)
            
            # Read sensor data and create the IMU state dictionary
            imuState = {
                "log_time": str(datetime.datetime.now()),
                "gyro_x": f"{sox.acceleration[0]:.2f}",
                "gyro_y": f"{sox.acceleration[1]:.2f}",
                "gyro_z": f"{sox.acceleration[2]:.2f}",
            }
            
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
            
            # Open the FIFO for writing
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            
            # Convert the IMU state to JSON format and write to the FIFO
            imuState = json.dumps(imuState, indent=4)
            posix.write(fifo_fd, imuState.encode())
            posix.close(fifo_fd)
            
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        oldTime = time.time()
        start_latch = 0
