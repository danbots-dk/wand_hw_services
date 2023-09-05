# wand_hw_services
This reposity keeps all hw dependent services which offer multi user connextivity

```
pip install -r requirements.txt

sudo cp io/ioLib.py /usr/lib/python3.9 
```

## Battery service
This service collect battery and power status
[Specification](SPEC_battery.md)

## IMU service
This service collect imu rotation data
[Specification](SPEC_imu.md)


## IO service
This service writes and collects data to and from various IO sensors
[Specification](SPEC_io.md)

## Eeprom library
This service writes and collects data to and from various IO sensors
[Specification](SPEC_eeprom.md)

