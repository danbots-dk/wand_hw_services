#!/bin/python3
import board
import busio
import digitalio
import RPi.GPIO as GPIO
import posix
import errno
from ioLib import IOexpander
import time
import json
import datetime
import threading
import os
import fcntl
import logging

# Initialize the logging module
logging.basicConfig(filename='/home/alexander/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize I2C and IOexpander
i2c = board.I2C()
ioService = IOexpander(i2c)

# Define the paths for the named pipes (FIFO)
WRITE_PIPE_NAME = "/tmp/io_stats"
READ_PIPE_NAME = "/tmp/io_conf"

# Create the named pipes if they don't exist
if not os.path.exists(WRITE_PIPE_NAME):
    os.mkfifo(WRITE_PIPE_NAME)
if not os.path.exists(READ_PIPE_NAME):
    os.mkfifo(READ_PIPE_NAME)

# Path to the lock file
lock_file = "/var/lock/i2c_lock"

# Create the lock file if it doesn't exist, or open it for reading and writing
if not os.path.isfile(lock_file):
    with open(lock_file, "w") as f:
        f.write("")
    f.close()

# Function for writing data to the FIFO
def write_to_fifo():
    update_rate = 0.1
    while True:
        try:
            ioInput = {
                "log_time": str(datetime.datetime.now()),
                "cap1val": ioService.getCap1Val(),
                "cap2val": ioService.getCap2Val(),
                "killSig": ioService.OnOff_interruptSig
            }
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            ioInput = json.dumps(ioInput, indent=4)
            posix.write(fifo_fd, ioInput.encode())
            posix.close(fifo_fd)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        time.sleep(update_rate)

# Function for reading data from the FIFO
def read_from_fifo():
    while True:
        try:
            logging.info("Reading from FIFO")
            fifo_fd = posix.open(READ_PIPE_NAME, posix.O_RDONLY)
            buffer_size = 1024
            data = posix.read(fifo_fd, buffer_size)
            posix.close(fifo_fd)
            data = json.loads(str(data.decode()))

            
            logging.info("Received data from FIFO: %s", data)
            # Obtain I2C lock
            lock = open(lock_file, "r+")
            fcntl.flock(lock, fcntl.LOCK_EX)
            
            ioService.sendKillSig(data["sendKillSig"])
            ioService.setBuzzer(data["setBuzzer"])
            ioService.setSpeaker(data["setSpeaker"])
            ioService.setBootloader(data["setBootloader"])
            ioService.setFlash(data["setFlash"])
            ioService.setDias(data["setDias"])
            logging.info("Received data from FIFO: %s", data["setIndicatorLED"])
            ioService.setIndicatorLED(data["setIndicatorLED"])
            
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()

        except:
            pass

if __name__ == "__main__":
    logging.info("Script started")

    # Create separate threads for read and write operations
    write_thread = threading.Thread(target=write_to_fifo)
    read_thread = threading.Thread(target=read_from_fifo)

    # Start the threads
    write_thread.start()
    read_thread.start()

    # Wait for the threads to complete
    write_thread.join()
    read_thread.join()
