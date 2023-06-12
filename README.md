# wand_hw_services
This reposity keeps all hw dependent services which offer multi user connextivity

## Battery service

This service collect battery and power status and provide a multi user interface

[Specification](SPEC_battery.md)

## Button/LED service

This service collect information from buttons and turn on and off the leds

[Specification](SPEC_button.md)

## IO service

This service collects data from the following services and writes to a FIFO buffer located at /tmp/io_stats
* Battery
  * batteryVoltage ([V])
  * batteryChargePercent ([%])
  * estimatedTimeForFullRecharge (time until fully charged, set to 999 when discharging)
  * estimatedTimeForFullDischarge (time until fully discharged, set to 999 when charging)
  * Alert 
      * "Reset_indicator"
* IMU
* Standard IO
  * isBattery (True if powered by battery) 
  * isCharging (True if battery is being charged)
  * getCap1Val
  * getCap2Val
[Specification](SPEC_io.md)
