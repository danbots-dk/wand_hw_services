import board
import busio
import digitalio
import RPi.GPIO as GPIO
import posix
import errno
from MCP23008 import IOexpander
import time
import json
import datetime
import threading
import os

i2c = board.I2C()
WRITE_PIPE_NAME = "/tmp/IO_stats"
READ_PIPE_NAME = "/tmp/IO_conf"
ioService = IOexpander(i2c)

if not os.path.exists(WRITE_PIPE_NAME):
    os.mkfifo(WRITE_PIPE_NAME)

def write_to_fifo():
    while True:
        try:
            ioInput = {
                "log_time": str(datetime.datetime.now()),
                "cap1val": ioService.getCap1Val(),
                "cap2val": ioService.getCap2Val(),
            }
            # NONBLOCK uses more cpu but is up to date
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            #fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY)
            ioInput = json.dumps(ioInput, indent=4)
            posix.write(fifo_fd, ioInput.encode())
            posix.close(fifo_fd)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        time.sleep(60)

def read_from_fifo():
    while True:
        try:
            #print("reading")
            fifo_fd = posix.open(READ_PIPE_NAME, posix.O_RDONLY)
            buffer_size = 1024
            data = posix.read(fifo_fd, buffer_size)
            posix.close(fifo_fd)
            data = json.loads(str(data.decode()))
            ioService.sendKillSig(data["sendKillSig"])
            ioService.setBuzzer(data["setBuzzer"])
            ioService.setSpeaker(data["setSpeaker"])
            ioService.setBootloader(data["setBootloader"])
            ioService.setFlash(data["setFlash"])
            ioService.setDias(int(data["setDias"]))

            #print(data["sendKillSig"])
            
        except:
            pass

        

# Create separate threads for read and write operations
write_thread = threading.Thread(target=write_to_fifo)
read_thread = threading.Thread(target=read_from_fifo)

# Start the threads
write_thread.start()
read_thread.start()

# Wait for the threads to complete
write_thread.join()
read_thread.join()