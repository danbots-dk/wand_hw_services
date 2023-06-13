#!/bin/python3
import adafruit_max1704x
import os
import json
import datetime


class BatteryService():
    def __init__(self, i2c):
        #i2c = board.I2C()  

        self.cellVoltage = 0
        self.cellPercent = 0
        self.estimatedTimeForFullRecharge = 0
        self.estimatedTimeForDischarge = 0
        self.hibernating = 0
        self.alertStatus = "None"

        #self.battery_stats = "/tmp/batteryService_stats"
        #self.battery_conf = "/tmp/batteryService_conf"
        # Create the FIFO if it doesn't exist
        #if not os.path.exists(self.battery_stats):
        #    os.mkfifo(self.battery_stats)
        
        self.max17 = adafruit_max1704x.MAX17048(i2c)
        hex(self.max17.chip_version)
        hex(self.max17.chip_id)
        self.max17.quick_start = True

        self.set_resetVoltage()
        self.set_voltageAlertMin()
        self.set_voltageAlertMax()
        print("Battery service started!")


        # Below value and chip considers it a battery swap
    def set_resetVoltage(self, resetVoltage = 2.5):
        self.max17.reset_voltage = resetVoltage
        

# Hibernation mode reduces how often the ADC is read, for power reduction. There is an automatic
# enter/exit mode but you can also customize the activity threshold both as voltage and charge rate
# self.max17.activity_threshold = 0.2
# self.max17.hibernation_threshold = 5
# self.max17.hibernate()
# self.max17.wake()

# The alert pin can be used to detect when the voltage of the battery goes below or
# above a voltage, you can also query the alert in the loop.
    def set_voltageAlertMin(self, minVoltage = 3.5):
        self.max17.voltage_alert_min = minVoltage
    def set_voltageAlertMax(self, maxVoltage = 4.25):
        self.max17.voltage_alert_max = maxVoltage

    def get_cellVoltage(self):
        cellVoltage = self.max17.cell_voltage
        return cellVoltage
    
    def get_cellPercent(self):
        cellPercent = self.max17.cell_percent
        return cellPercent


    def get_TimeToCharge(self):
        try:
            if self.max17.charge_rate < 0:
                estimatedTimeToDischarge = (self.max17.cell_percent/(self.max17.charge_rate*(-1)))
                estimatedTimeToFullRecharge = 999
                #Hours_d = estimatedTimeForDischarge
                #Minutes_d = 60 * (Hours_d % 1)
                #Seconds_d = 60 * (Minutes_d % 1)
                #estimatedTimeForFullRecharge = f"{Hours_d}:{Minutes_d}:{Seconds_d}"
            else:
                estimatedTimeToFullRecharge = (100-self.max17.cell_percent)/self.max17.charge_rate
                estimatedTimeToDischarge = 999
                #Hours_r = estimatedTimeForFullRecharge
                #Minutes_r = 60 * (Hours_r % 1)
                #Seconds_r = 60 * (Minutes_r % 1)
                #estimatedTimeForFullRecharge = f"{Hours_r}:{Minutes_r}:{Seconds_r}"
            return estimatedTimeToFullRecharge, estimatedTimeToDischarge
        except:
            # Important because charge rate can be zero on init (~2s)
            return 0, 0

    def get_HibernateState(self):
        self.hibernating = self.max17.hibernating

    def get_Alerts(self):
        if self.max17.active_alert:
            if self.max17.reset_alert:
                alertStatus = "Reset_indicator"
                self.max17.reset_alert = False  # clear the alert

            if self.max17.voltage_high_alert:
                alertStatus = "Voltage_high"
                self.max17.voltage_high_alert = False  # clear the alert

            if self.max17.voltage_low_alert:
                alertStatus = "Voltage_low"
                self.max17.voltage_low_alert = False  # clear the alert

            if self.max17.voltage_reset_alert:
                alertStatus = "Voltage_reset"
                self.max17.voltage_reset_alert = False  # clear the alert

            if self.max17.SOC_low_alert:
                alertStatus = "Charge_low"
                self.max17.SOC_low_alert = False  # clear the alert

            if self.max17.SOC_change_alert:
                alertStatus = "Charge_changed"
                self.max17.SOC_change_alert = False  # clear the alert

        else:
            alertStatus = "None"

        return alertStatus


    def writeStats(self):
        timeToCharge = self.get_TimeToCharge()
        batteryInfo = {
        "log_time": str(datetime.datetime.now()),
        "batteryVoltage": f"{self.get_cellVoltage():.2f}",
        "batteryChargePercent": f"{self.get_cellPercent():.2f}",
        "estimatedTimeForFullRecharge": f"{timeToCharge[0]:.2f}",
        "estimatedTimeForDischarge": f"{timeToCharge[1]:.2f}",
        "Alert": self.get_Alerts()
            }
        return batteryInfo

        


if __name__ == "__main__":
    import time
    import board
    i2c = board.I2C()  
    bat = BatteryService(i2c)
    while 1:
        bat.writeState()
        time.sleep(1)


