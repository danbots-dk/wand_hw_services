from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import board
import json
import time 
import os
import datetime


i2c = board.I2C()
sox = LSM6DS3(i2c)

IO_stats = "/tmp/imu_stats"
if not os.path.exists(IO_stats):
    os.mkfifo(IO_stats)

while(1):
    imuState = {
        "log_time": str(datetime.datetime.now()),
        "gyro_x": f"{sox.acceleration[0]:.2f}",
        "gyro_y": f"{sox.acceleration[1]:.2f}",
        "gyro_z": f"{sox.acceleration[2]:.2f}",
            }
    IO_info = json.dumps(imuState, indent=4)
    fifo = open(IO_stats, "w")
    fifo.write(IO_info)
    fifo.close()

    #time.sleep(1)