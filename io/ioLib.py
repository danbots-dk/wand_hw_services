import time
from adafruit_mcp230xx.mcp23008 import MCP23008
import json
import digitalio
import RPi.GPIO as GPIO  
import datetime
import pigpio
import board
import neopixel
import adafruit_mcp4728
import os
import logging
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from tmp1075 import TMP1075




class IOexpander:
    def __init__(self,i2c):
        self.brdVersion = 1.8

        self.mcp = MCP23008(i2c)
        try:
            self.dac = adafruit_mcp4728.MCP4728(i2c, 0x62)
        except:
            try:
                self.dac = adafruit_mcp4728.MCP4728(i2c, 0x60)
            except:
                pass
        logging.basicConfig(filename='/var/log/io.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # IO expander
        self.state_pin = self.mcp.get_pin(0)
        self.state_pin.direction = digitalio.Direction.INPUT

        self.cap1 = self.mcp.get_pin(2)
        self.cap1.direction = digitalio.Direction.INPUT

        self.cap2 = self.mcp.get_pin(3)
        self.cap2.direction = digitalio.Direction.INPUT

        self.buzzer = self.mcp.get_pin(5)
        self.buzzer.direction = digitalio.Direction.OUTPUT

        self.bat_chg = self.mcp.get_pin(6)
        self.bat_chg.direction = digitalio.Direction.INPUT        
        
        self.bat_pg = self.mcp.get_pin(7)
        self.bat_pg.direction = digitalio.Direction.INPUT


        # RPi GPIO
        self.bootLoader = 4
        self.DIAS = 12
        self.flash = 13
        self.batInterrupt_pin = 17        
        self.OnOff_kill = 22
        self.OnOff_interrupt_button = 27

        GPIO.setup(self.bootLoader, GPIO.OUT)
        GPIO.setup(self.DIAS, GPIO.OUT)
        GPIO.setup(self.flash, GPIO.OUT)
        GPIO.setup(self.batInterrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.OnOff_interrupt_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Neopixel
        pixel_pin = board.D10
        num_pixels = 4
        ORDER = neopixel.RGB
        brightness = 0.5
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=brightness, pixel_order=ORDER, auto_write=False
        )

        self.OnOff_interruptSig = 0
        self.createOnOffInterrupt()
        logging.info("io service started")

        self.tmp1075 = TMP1075(0x48)

    def OnOff_interrupt(self, channel):
        self.OnOff_interruptSig = 1

    def createOnOffInterrupt(self):
        GPIO.add_event_detect(self.OnOff_interrupt_button, GPIO.FALLING, callback=self.OnOff_interrupt, bouncetime=100)

    def createBatAlertInterrupt(self):
        GPIO.add_event_detect(self.batInterrupt_pin, GPIO.FALLING, callback=self.bat_interrupt, bouncetime=100)

    def sendKillSig(self,state):
        # TODO: insert clean up routine
        if state == True:
            time.sleep(1)
            GPIO.setup(self.OnOff_kill, GPIO.OUT)
        else:
            pass


    def setFlash(self, val):
        if(self.brdVersion > 1.8):
            self.dac.normalized_value = val
        else:        
            if val > 0 :
                GPIO.output(self.flash, GPIO.HIGH)
            else:
                GPIO.output(self.flash, GPIO.LOW)

    def setDias(self, val):
        if(self.brdVersion > 1.8):
            self.dac.normalized_value.channel_a = val
            self.dac.normalized_value.channel_b = val
        else: 
            if val > 0:
                GPIO.output(self.DIAS, GPIO.HIGH)
            else:
                GPIO.output(self.DIAS, GPIO.LOW)
    
    def setIndicatorLED(self, val):
        self.pixels[(val[0])] = ((val[1]),(val[2]),(val[3]))
        self.pixels.show()
        
        
    def setBuzzer(self, state):
        self.buzzer.value = state
        return 1

    def setSpeaker(self, state):
        #self.speaker.value = state
        pass
        #return 1

    def setBootloader(self, state):
        # TODO: insert clean up routine
        
        if state == True:
            time.sleep(1)
            GPIO.output(self.bootLoader, GPIO.HIGH)
            os.system("shutdown -h 0 -r")
        else:
            GPIO.output(self.bootLoader, GPIO.LOW) 
        

    def isBattery(self):
        # 1: battery powered
        # 0: USB powered
        return self.bat_pg.value
    
    def isCharging(self):
        # 1: is charging
        # 0: is not charging
        return self.bat_chg.value

    def getCap1Val(self):
        return self.cap1.value
    
    def getCap2Val(self):
        return self.cap2.value

    def carrier_board_temp(self):
        return self.tmp1075.get_temperature()

    def writeStats(self):
        ioInfo = {
        "log_time": str(datetime.datetime.now()),
        "cap1val": f"{self.getCap1Val()}",
        "cap2val": f"{self.getCap2Val()}",
        "isBattery": f"{self.isBattery()}",
        "isCharging": f"{self.isCharging()}",
        "killSig": f"{self.OnOff_interruptSig}",
        "carrier_temp": f"{self.carrier_board_temp()}"
            }
        return ioInfo

    def readConf(self,data=None):
        if data == None:
            data = {
                "sendKillSig": False,
                "setBuzzer": False,
                "setSpeaker": False,
                "setBootloader": False,
                "setFlash": 0,
                "setDias": 0,
                "setIndicatorLED": [0,0,0,0]
            }      
        self.sendKillSig(data["sendKillSig"])
        self.setBuzzer(data["setBuzzer"])
        self.setSpeaker(data["setSpeaker"])
        self.setBootloader(data["setBootloader"])
        self.setDias(data["setDias"])
        self.setFlash(data["setFlash"])
        self.setIndicatorLED(data["setIndicatorLED"])

        return "1"

if __name__ == "__main__":
    import board
    i2c = board.I2C()
    io = IOexpander(i2c)
    while(1):
        print(f"pg: {io.get_temperature()}")
        print(f"chg: {io.isCharging()}")
        time.sleep(2)