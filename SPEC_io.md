
# Specification of io service

## OS requirements

Raspberry PI Os lite:  2023-05-03-raspios-bullseye-armhf-lite

## Installation and uninstallation of service

```
pip install -r requirements.txt
sudo cp ioService/ioService.py /usr/local/bin/
sudo cp ioService/ioService.service /etc/systemd/system/

sudo service ioService start
```


## Service description
The service implements functionality to set state of certain IO's, and to output the state of others. This is done in a non blocking fashion using threading and with minimal cpu usage.

The following IO's can be set by the user:
- Send kill signal to cut the power supply
- Set buzzer on/off
  - Timer
- Set vibration motor on/off
  - Timer  
- Enable the bootloader stage for next reboot
- Flash LED
- Dias LED
- Set 4 different indicator LED's
  - idx 0 is on the carrier pcb
  - idx 1 is top capacitive touch pcb
  - idx 2 is bottom capactive touch pcb
  - idx 3 is the back capacitive touch pcb
  - r,g,b is in range 0-255

The following input can be read by the user:
- Both fron capacitive touch buttons
- Capacitive touch button at the rear
- Powerdown signal from on/off button
  - When press is detected the variable latches so that it is always detected.

The service shutsdown gracefully within 3 seconds

## Configuration of service
No configuration except installation is needed.

## User interface


The input data is available at /tmp/io_stats in the following JSON structure 
```javascript
ioInput =  {
    "log_time": dateTime,
    "cap1val": 0/1,
    "cap2val": 0/1,
    "killSig": 0/1,
            }     
```

The user can configure the IO's by writing a named pipe located at /tmp/io_conf using the specified API.
```javascript
IO_write = {
        "sendKillSig": true/false,
        "setBuzzer": true/false,
        "setSpeaker": true/false,
        "setBootloader": true/false,
        "setDias": 0.0-1.0,
        "setFlash": 0.0-1.0,
        "setIndicatorLED": [idx, r,g,b]
    }
```
