# Documentation for eeprom library

## OS requirements

Raspberry PI Os lite:  2023-05-03-raspios-bullseye-armhf-lite

## Installation and uninstallation of service

```
pip install -r requirements.txt
sudo cp eepromLib/cat24c512.py /usr/lib/python3.9/cat24c512.py


```


## Library description

The library provides an api to the Eeprom IC 24C512. Further, it indexes the memory so that various version of PCB's, libraries etc. have their own section and can be easily accessed. 

### API
The following functions can be used:
```
set_version(val, idx)
get_version(idx)
get_all_version()
```
val and idx are of type string.

set_version() sets the version of the desired object. Idx is used to specify which object.
A string is to be used as idx, since a dict is used to refer to a value. The dict can be seen below:
```
eeprom_idx = {"carrier": 0,
            "front_touch": 10,
            "on_off": 20,
            "flash_flex": 30,
            "img_version": 40,
            "img_install_date": 50,
            "io_service": 60,
            "battery_service": 70,
            "imu_service": 80,
            "eeprom": 90
             }
```

For example if one whishes to set the version value of on_off to 1.0, the following command should be used
```
set_version("1.0", "on_off")
```




