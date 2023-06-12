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
  * mainPowerConnected 
  * batteryVoltage ([V])
  * batteryChargePercent ([%])
  * estimatedTimeForFullRecharge (time until fully charged, set to 999 when discharging)
  * estimatedTimeForFullDischarge (time until fully discharged, set to 999 when charging)
  * Alert 
      * "Reset_indicator" - bat IC has been reset by battery swap or similar
      * "Voltage_high" - battery voltage above 4.25V
      * "Voltage_low" - battery voltage below 3.5
      * "Voltage_reset" - Unsure
      * "Charge_low" - Unsure at what charge
      * "Charge_changed" - Unsure


* IMU
  * gyro_x
  * gyro_y
  * gyro_z 


* Standard IO
  * isBattery (True if powered by battery) 
  * isCharging (True if battery is being charged)
  * getCap1Val
  * getCap2Val
[Specification](SPEC_io.md)
