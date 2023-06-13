# Specification of battery service

## OS requirements

Raspberry PI Os lite:  2023-05-03-raspios-bullseye-armhf-lite

## Installation and uninstallation of service

```
pip install -r requirements.txt
sudo cp imuService/imuService.py /usr/local/bin/
sudo cp imuService/imuService.service /etc/systemd/system/

sudo service imuService start
```


## Service description

The service collect infromation from hw and provide the users whith the following information

- Rotation around x-axis
- Rotation around y-axis
- Rotation around z-axis

The range of a full rotation around any given axis is from -10 to 10

x-axis is perpendicular to the length of the wand
y-axis runs along the length of the wand
z-axis is perpendicular to the length of the wand going naturally upwards 

## Configuration of service
No configuration needed.

## User interface

The data is written to a named pipe available at /tmp/imu_stats in the following JSON structure 
```javascript
imuState = {
            "log_time": str(datetime.datetime.now()),
            "gyro_x": f"{sox.acceleration[0]:.2f}",
            "gyro_y": f"{sox.acceleration[1]:.2f}",
            "gyro_z": f"{sox.acceleration[2]:.2f}",
            }     
```

