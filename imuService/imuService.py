from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import board
import json
import time 
import os
import datetime
import posix
import errno
import fcntl


i2c = board.I2C()
sox = LSM6DS3(i2c)

WRITE_PIPE_NAME = "/tmp/imu_stats"
delay_s = 0.1
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
        try:
            # Obtain i2c lock
            lock = open(lock_file, "r+")
            fcntl.flock(lock, fcntl.LOCK_EX)
            imuState = {
                "log_time": str(datetime.datetime.now()),
                "gyro_x": f"{sox.acceleration[0]:.2f}",
                "gyro_y": f"{sox.acceleration[1]:.2f}",
                "gyro_z": f"{sox.acceleration[2]:.2f}",
            }
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
            # NONBLOCK uses more cpu but data is up to date
            fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY | posix.O_NONBLOCK)
            #fifo_fd = posix.open(WRITE_PIPE_NAME, posix.O_WRONLY)
            imuState = json.dumps(imuState, indent=4)
            posix.write(fifo_fd, imuState.encode())
            posix.close(fifo_fd)
            
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                pass  # try later

        oldTime = time.time()
        start_latch = 0

    #time.sleep(1)