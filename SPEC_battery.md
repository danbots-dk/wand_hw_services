# Specification of battery service

## OS requirements

Raspberry PI Os lite:  2023-05-03-raspios-bullseye-armhf-lite

## Installation and uninstallation of service

```
pip install -r requirements.txt
sudo cp batteryService/MAX17048.py /usr/local/bin/
sudo cp batteryService/batteryService.py /usr/local/bin/
sudo cp batteryService/batteryService.service /etc/systemd/system/

sudo service batteryService start
```


## Service description

The service collect infromation from hw and provide the users whith the following information

- Is the battery charging
- Is the wand powered by battery
- Battery voltage
- Battery charge percent
- Estimate time for full recharge
- Estimatted time for discharge
- Battery voltage too low

The service shutsdown gracefully within 3 seconds

## Configuration of service
The service relies on the MAX17048 IC which automatically calibrates for charge leves, time estimation, etc. Hence little input from the user is needed.

## User interface
The data is written to a named pipe available at /var/run/wand/battery_stats in the following JSON structure 
```javascript
batteryInfo = {
        "log_time": datetime,
        "batteryVoltage": cellVoltage [V],
        "batteryChargePercent": cellPercent [%],
        "estimatedTimeForFullRecharge": [decimal hours],
        "estimatedTimeForDischarge": [decimal hours],
        "Alert": alert message,
        "isCharging": true/false,
        "isBattery": true/false,
        "lowVoltageDetected" true/false
            }         
```
