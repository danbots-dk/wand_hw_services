# SPDX-FileCopyrightText: 2021 codenio (Aananth K)
# SPDX-License-Identifier: MIT
#import board
#import adafruit_mcp4728
#
#i2c = board.I2C()  # uses board.SCL and board.SDA
## i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#mcp4728 = adafruit_mcp4728.MCP4728(i2c, 0x60)
#
#mcp4728.channel_a.value = 0  # Voltage = VDD
#mcp4728.channel_d.value = 0  # 0V
#
#mcp4728.save_settings()  # save current voltages into EEPROM
#
#print("Settings Saved into EEPROM")
#
#input("Press Enter to modify the channel outputs...")
#
#mcp4728.channel_a.value = 0  # Modify output
#mcp4728.channel_d.value = 0  # Modify output
#
#print("Channel Outputs Modified")
#
#input("Press Enter to invoke General Call Reset ...")
#
#mcp4728.reset()  # reset MCP4728



#import time
#
## Import the MCP4725 module.
#import Adafruit_MCP4725
#
## Create a DAC instance.
#dac = Adafruit_MCP4725.MCP4725(address=0x60)
#
## Note you can change the I2C address from its default (0x62), and/or the I2C
## bus by passing in these optional parameters:
##dac = Adafruit_MCP4725.MCP4725(address=0x49, busnum=1)
#
## Loop forever alternating through different voltage outputs.
#print('Press Ctrl-C to quit...')
#while True:
#    print('Setting voltage to 0!')
#    dac.set_voltage(0)
#    time.sleep(2.0)
#    print('Setting voltage to 1/2 Vdd!')
#    dac.set_voltage(2048)  # 2048 = half of 4096
##    time.sleep(2.0)
##    print('Setting voltage to Vdd!')
##    dac.set_voltage(4096, True)
##    time.sleep(2.0)
#
#import smbus
#
## I2C address based on pin 2 (A0) and pin 8 (A1)
#DAC_ADR_A0 = 0
#DAC_ADR_A1 = 0
#
## Registers
#DAC_WIPER_REG0 = 0x00
#DAC_WIPER_REG1 = 0x01
#DAC_VREF_REG = 0x08
#DAC_POWERDOWN_REG = 0x09
#DAC_GAIN_REG = 0x0A
#
## General Call Commands
#I2C_RESET = 0x06
#I2C_WAKE = 0x0A
#
## Register settings
#
## VREF
#DAC_VREF_VDD = 0b00  # VDD is the reference
#DAC_VREF_INTERNAL = 0b01  # internal bandgap ref of 1.214V
#DAC_VREF_EXT_UNBUFF = 0b10  # external unbuffered reference - does not use the internal opamp
#DAC_VREF_EXT_BUFF = 0x11  # external buffered reference - uses the internal opamp
#
## POWER
#DAC_PWR_NORMAL = 0b00  # Normal operation
#DAC_PWR_DOWN_1K = 0b01  # Powered down, with 1kohm resistor to ground on outputs
#DAC_PWR_DOWN_100K = 0b10  # Powered down, with 100kohm resistor to ground on outputs
#DAC_PWR_DOWN_HIZ = 0b11  # Powered down, with Hi-Z on outputs
#
## GAIN
#DAC_GAIN_1X = 0  # channel 1, output gain of 1
#DAC_GAIN_2X = 1  # channel 1, output gain of 2
#
## STATUS - Read only
#DAC_STATUS_POR = 1 << 7  # A 1 on this bit indicates POR/BOR event occurred since last read, guessing it clears after reading
#DAC_STATUS_MTPMA = 1 << 6  # A 1 indicates memory is being accessed
#
#DAC_ADR_DEFAULT = 0x60
#
#class MCP47CXBXX_DAC:
#    def __init__(self):
#        self.bus = smbus.SMBus(1)  # Use I2C bus number 1, you may need to change this based on your setup
#        self.DAC_ADDRESS = DAC_ADR_DEFAULT
#        self.DAC_RESOLUTION = 0
#        self.dac_chcount = 0
#        self.DAC_MAX_VALUE = 0
#
#    def begin(self, resolution=8, channel_count=2, i2c_address=DAC_ADR_DEFAULT, clock=200000):
#        status_flag = 0
#
#        #self.bus.open(1)
#        self.DAC_ADDRESS = i2c_address
#        self.DAC_RESOLUTION = resolution
#        self.dac_chcount = channel_count
#
#        if self.DAC_RESOLUTION == 8:
#            self.DAC_MAX_VALUE = 255
#        elif self.DAC_RESOLUTION == 10:
#            self.DAC_MAX_VALUE = 1023
#        elif self.DAC_RESOLUTION == 12:
#            self.DAC_MAX_VALUE = 4095
#        else:
#            status_flag = 0
#
#        status_flag |= self.setOutput(DAC_WIPER_REG0, 1)
#        status_flag |= self.setOutput(DAC_WIPER_REG1, 2)
#
#        return status_flag
#
#    def setOutput(self, channel, value, continuous=False):
#        status_flag = 0
#        dac_register = 0
#        print(f"first: {value}")
#        if channel == 0:
#            dac_register = DAC_WIPER_REG0
#        elif channel == 1:
#            dac_register = DAC_WIPER_REG1
#        else:
#            status_flag = 7
#
#        if value > self.DAC_MAX_VALUE:
#            value = self.DAC_MAX_VALUE
#            status_flag = 8
#        print(f"1.5: {value}")
#
#
#        if self.DAC_RESOLUTION == 8:
#            value &= 0b0000000011111111
#        if self.DAC_RESOLUTION == 10:
#            value &= 0b0000001111111111
#        if self.DAC_RESOLUTION == 12:
#            value &= 0b0000111111111111
#        print(f"1.8: {value}")
#        print(f"second: {(value) & 0xFF}")
#
#        status_flag |= self.write(dac_register, (value) & 0xFF, value & 0xFF, not continuous)
#
#        return status_flag
#
#    def setPwr(self, channel_0_setting, channel_1_setting):
#        value_LSB = (channel_1_setting << 2) & 0b00001100 | (channel_0_setting) & 0b00000011
#        status_flag = self.write(DAC_POWERDOWN_REG, 0, value_LSB)
#        return status_flag
#
#    def setVref(self, channel_0_setting, channel_1_setting):
#        value_LSB = (channel_1_setting << 2) & 0b00001100 | (channel_0_setting) & 0b00000011
#        status_flag = self.write(DAC_VREF_REG, 0, value_LSB)
#        return status_flag
#
#    def setGain(self, channel_0_setting, channel_1_setting):
#        value_MSB = (channel_1_setting << 1) & 0b00000010 | (channel_0_setting) & 0b00000001
#        status_flag = self.write(DAC_GAIN_REG, value_MSB, 0)
#        return status_flag
#
#    def readOutput(self, channel):
#        if channel == 0:
#            channel = DAC_WIPER_REG0
#        elif channel == 1:
#            channel = DAC_WIPER_REG1
#        else:
#            return 0
#
#        value = self.read(channel)
#        return value
#
#    def wake(self):
#        self.generalCommand(I2C_WAKE)
#
#    def reset(self):
#        self.generalCommand(I2C_RESET)
#
#    def generalCommand(self, command):
#        self.bus.write_byte_data(0x00, command, 0x00)
#
#    def write(self, command, value_MSB, value_LSB, sendStop=True):
#        status_flag = 0
#
#        self.bus.write_byte_data(self.DAC_ADDRESS, (command << 3) & 0xF8, value_MSB)
#        self.bus.write_byte_data(self.DAC_ADDRESS, (command << 3) & 0xF8, value_LSB)
#
#        status_flag |= self.bus.read_byte_data(self.DAC_ADDRESS, 0x00)
#
#        if status_flag == 0:
#            status_flag = 6
#        if status_flag == 1:
#            status_flag = 0
#
#
#        return status_flag
#
#    def read(self, command):
#        status_flag = 0
#
#        self.bus.write_byte_data(self.DAC_ADDRESS, (command << 3) & 0xF8 | 0b00000110)
#
#        if status_flag == 0:
#            status_flag = 6
#        if status_flag == 1:
#            status_flag = 0
#
#        status_flag |= self.bus.end_transmission(False)
#
#        value = self.bus.read_word_data(self.DAC_ADDRESS, 0x00)
#        return value
#
#
## Usage example
#if __name__ == '__main__':
#    dac = MCP47CXBXX_DAC()
#
#    # Begin I2C communication and get current values
#    dac.begin()
#
#    # Reset the device
#    #dac.reset()
#
#    # Set Vref to internal (1) and gain to 1x
#    #dac.setVref(1, 1)
#    #dac.setGain(0, 0)
#
#    # Set DAC output voltages
#    dac.setOutput(0, 20)
#    dac.setOutput(1, 20)
#
#    # Read the current values
#    #value0 = dac.readOutput(0)
#    #value1 = dac.readOutput(1)
#
#    #print("Value Channel 0:", value0)
#    #print("Value Channel 1:", value1)
#
#
#
#
















# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#import board
#import adafruit_mcp4728
#
#MCP4728_DEFAULT_ADDRESS = 0x60
#MCP4728A4_DEFAULT_ADDRESS = 0x64
#
#i2c = board.I2C()  # uses board.SCL and board.SDA
## i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
##  use for MCP4728 variant
#mcp4728 = adafruit_mcp4728.MCP4728(i2c, adafruit_mcp4728.MCP4728_DEFAULT_ADDRESS)
##  use for MCP4728A4 variant
##  mcp4728 = adafruit_mcp4728.MCP4728(i2c, adafruit_mcp4728.MCP4728A4_DEFAULT_ADDRESS)
#
##mcp4728.channel_a.value = 0  # Voltage = VDD
##mcp4728.channel_b.value = 0  # VDD/2
##mcp4728.channel_c.value = 0  # VDD/4
#mcp4728.reset()  # reset MCP4728
#mcp4728.channel_d.value = 0  # 0V


import smbus2

# Define the I2C bus number (typically 1 on most Raspberry Pi models)
I2C_BUS = 1

# Initialize the I2C bus
i2c_bus = smbus2.SMBus(I2C_BUS)

class MCP47CVB02:
    # Define the DAC's I2C address
    DAC_ADDRESS = 0x60

    def __init__(self, i2c_bus):
        self.i2c_bus = i2c_bus

    def set_output_voltage(self, channel, voltage):
        if channel == 0:
            command = 0x00  # DAC0 Write
        elif channel == 1:
            command = 0x04  # DAC1 Write
        else:
            raise ValueError("Invalid channel. Use 0 for DAC0 or 1 for DAC1.")

        # Calculate the 12-bit data value based on the voltage (assuming Vref = 5V)
        data = int(voltage / 5 * 255)
        print(0x00+data)
        # Send the data over I2C
        self.i2c_bus.write_word_data(self.DAC_ADDRESS, command, data)

# Initialize the DAC object
dac = MCP47CVB02(i2c_bus)

# Set the output voltage of DAC0 to 2.5V
dac.set_output_voltage(channel=0, voltage=1)

# Set the output voltage of DAC1 to 3.3V
dac.set_output_voltage(channel=1, voltage=1)
