#!/bin/python3
import adafruit_max1704x
import os
import json
import datetime
from adafruit_mcp230xx.mcp23008 import MCP23008
import digitalio

class BatteryService():
    """
    A class that provides battery-related functionality using the adafruit_max1704x library.

    Attributes:
        cellVoltage (float): The voltage of the battery cell.
        cellPercent (float): The remaining charge percentage of the battery.
        estimatedTimeForFullRecharge (float): The estimated time for the battery to fully recharge.
        estimatedTimeForDischarge (float): The estimated time for the battery to discharge completely.
        hibernating (bool): Indicates if the battery is in hibernation mode.
        alertStatus (str): The current alert status of the battery.

    Methods:
        __init__(self, i2c): Initializes the BatteryService class.
        set_resetVoltage(self, resetVoltage): Sets the reset voltage for the battery.
        set_voltageAlertMin(self, minVoltage): Sets the minimum voltage alert threshold for the battery.
        set_voltageAlertMax(self, maxVoltage): Sets the maximum voltage alert threshold for the battery.
        get_cellVoltage(self): Retrieves the voltage of the battery cell.
        get_cellPercent(self): Retrieves the remaining charge percentage of the battery.
        get_TimeToCharge(self): Calculates the estimated time for the battery to recharge or discharge completely.
        get_HibernateState(self): Retrieves the hibernation state of the battery.
        get_Alerts(self): Retrieves the current alert status of the battery.
        writeStats(self): Writes battery-related statistics to a JSON object.

    """

    def __init__(self, i2c):
        """
        Initializes the BatteryService class.

        Args:
            i2c: The I2C bus object used for communication with the battery.

        """
        self.cellVoltage = 0
        self.cellPercent = 0
        self.estimatedTimeForFullRecharge = 0
        self.estimatedTimeForDischarge = 0
        self.hibernating = False
        self.alertStatus = "None"

        self.max17 = adafruit_max1704x.MAX17048(i2c)
        hex(self.max17.chip_version)
        hex(self.max17.chip_id)
        self.max17.quick_start = True

        self.set_resetVoltage()
        self.set_voltageAlertMin()
        self.set_voltageAlertMax()
        self.lowVoltageDetected = False


        self.mcp = MCP23008(i2c)

        self.bat_pg = self.mcp.get_pin(0)
        self.bat_pg.direction = digitalio.Direction.INPUT

        self.bat_chg = self.mcp.get_pin(1)
        self.bat_chg.direction = digitalio.Direction.INPUT


        print("Battery service started!")

    def set_resetVoltage(self, resetVoltage=2.5):
        """
        Sets the reset voltage for the battery.

        Args:
            resetVoltage (float): The reset voltage value to set. Default is 2.5V.

        """
        self.max17.reset_voltage = resetVoltage

    def set_voltageAlertMin(self, minVoltage=3.5):
        """
        Sets the minimum voltage alert threshold for the battery.

        Args:
            minVoltage (float): The minimum voltage threshold value to set. Default is 3.5V.

        """
        self.max17.voltage_alert_min = minVoltage

    def set_voltageAlertMax(self, maxVoltage=4.25):
        """
        Sets the maximum voltage alert threshold for the battery.

        Args:
            maxVoltage (float): The maximum voltage threshold value to set. Default is 4.25V.

        """
        self.max17.voltage_alert_max = maxVoltage

    def get_cellVoltage(self):
        """
        Retrieves the voltage of the battery cell.

        Returns:
            float: The voltage of the battery cell [V].

        """
        cellVoltage = self.max17.cell_voltage
        return cellVoltage

    def get_cellPercent(self):
        """
        Retrieves the remaining charge percentage of the battery.

        Returns:
            float: The remaining charge percentage of the battery [%].

        """
        cellPercent = self.max17.cell_percent
        return cellPercent

    def get_TimeToCharge(self):
        """
        Calculates the estimated time for the battery to recharge or discharge completely.

        Returns:
            float: The estimated time for the battery to fully recharge.
            float: The estimated time for the battery to discharge completely.

        """
        try:
            if self.max17.charge_rate < 0:
                estimatedTimeToDischarge = (self.max17.cell_percent / (self.max17.charge_rate * (-1)))
                estimatedTimeToFullRecharge = 999
            else:
                estimatedTimeToFullRecharge = (100 - self.max17.cell_percent) / self.max17.charge_rate
                estimatedTimeToDischarge = 999
            return estimatedTimeToFullRecharge, estimatedTimeToDischarge
        except:
            return 0, 0

    def get_HibernateState(self):
        """
        Retrieves the hibernation state of the battery.

        """
        self.hibernating = self.max17.hibernating

    def get_Alerts(self):
        """
        Retrieves the current alert status of the battery.

        Returns:
            str: The current alert status of the battery.

        """
        if self.max17.active_alert:
            if self.max17.reset_alert:
                alertStatus = "Reset_indicator"
                self.max17.reset_alert = False  # clear the alert

            if self.max17.voltage_high_alert:
                alertStatus = "Voltage_high"
                self.lowVoltageDetected = True
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
            self.lowVoltageDetected = False
            alertStatus = "None"

        return alertStatus


    def isBattery(self):
        # 1: battery powered
        # 0: USB powered
        return self.bat_pg.value
    
    def isCharging(self):
        # 1: is charging
        # 0: is not charging
        return self.bat_chg.value
    

    def writeStats(self):
        """
        Writes battery-related statistics to a JSON object.

        Returns:
            dict: A JSON object containing battery-related statistics.

        """
        timeToCharge = self.get_TimeToCharge()
        batteryInfo = {
            "log_time": str(datetime.datetime.now()),
            "batteryVoltage": f"{self.get_cellVoltage():.2f}",
            "batteryChargePercent": f"{self.get_cellPercent():.2f}",
            "estimatedTimeForFullRecharge": f"{timeToCharge[0]:.2f}",
            "estimatedTimeForDischarge": f"{timeToCharge[1]:.2f}",
            "Alert": self.get_Alerts(),
            "lowVoltageDetected": self.lowVoltageDetected,
            "isBattery": f"{self.isBattery()}",
            "isCharging": f"{self.isCharging()}",
        }
        return batteryInfo


if __name__ == "__main__":
    import time
    import board

    i2c = board.I2C()
    bat = BatteryService(i2c)

    while True:
        bat.writeStats()
        time.sleep(1)
