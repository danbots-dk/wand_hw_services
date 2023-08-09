import time
from adafruit_mcp230xx.mcp23008 import MCP23008
import json
import digitalio
import RPi.GPIO as GPIO  
import datetime
import pigpio

class IOexpander:
    def __init__(self,i2c):
        self.mcp = MCP23008(i2c)

        # IO expander
        #self.state_pin = self.mcp.get_pin(6)
        #self.state_pin.direction = digitalio.Direction.INPUT
        
        # IO expander
        #self.state_pin = self.mcp.get_pin(6)
        #self.state_pin.direction = digitalio.Direction.INPUT
        
        self.bat_pg = self.mcp.get_pin(7)
        self.bat_pg.direction = digitalio.Direction.INPUT

        self.bat_chg = self.mcp.get_pin(6)
        self.bat_chg.direction = digitalio.Direction.INPUT

        self.buzzer = self.mcp.get_pin(3)
        self.buzzer.direction = digitalio.Direction.OUTPUT

        self.cap1 = self.mcp.get_pin(2)
        self.cap1.direction = digitalio.Direction.INPUT

        self.cap2 = self.mcp.get_pin(4)
        self.cap2.direction = digitalio.Direction.INPUT

        # RPi GPIO
        self.bootLoader = 4
        self.OnOff_interrupt_button = 27
        self.OnOff_kill = 22
        self.batInterrupt_pin = 17
        self.DIAS = 12
        self.flash = 13

        GPIO.setup(self.bootLoader, GPIO.OUT)
        GPIO.setup(self.DIAS, GPIO.OUT)
        GPIO.setup(self.flash, GPIO.OUT)
        GPIO.setup(self.batInterrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.OnOff_interrupt_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.pigpio = pigpio.pi()

    def createOnOffInterrupt(self):
        GPIO.add_event_detect(self.OnOff_interrupt_button, GPIO.FALLING, callback=self.OnOff_interrupt, bouncetime=100)

    def createBatAlertInterrupt(self):
        GPIO.add_event_detect(self.batInterrupt_pin, GPIO.FALLING, callback=self.bat_interrupt, bouncetime=100)

    def sendKillSig(self,state):
        if state == True:
            GPIO.setup(self.OnOff_kill, GPIO.OUT)
        else:
            pass
        

    def setFlash(self, state):        
        if state == True:
            GPIO.output(self.flash, GPIO.HIGH)
        else:
            GPIO.output(self.flash, GPIO.LOW)

    def setDias(self, state):
        if state == True:
            GPIO.output(self.DIAS, GPIO.HIGH)
        else:
            GPIO.output(self.DIAS, GPIO.LOW)
        
    def setBuzzer(self, state):
        ##self.buzzer.value = state
        #print(state)
        pass
        #return 1

    def setSpeaker(self, state):
        #self.speaker.value = state
        pass
        #return 1

    def setBootloader(self, state):
        if state == True:
            GPIO.output(self.bootLoader, GPIO.HIGH)
        else:
            GPIO.output(self.bootLoader, GPIO.LOW) 

    def isBattery(self):
        # 1: battery powered
        # 0: USB powered
        return self.bat_pg.value
    
    def isCharging(self):
        # 0: is charging
        # 1: is not charging
        return not(self.bat_chg.value)

    def getCap1Val(self):
        return self.cap1.value
    
    def getCap2Val(self):
        return self.cap2.value

    def writeStats(self):
        ioInfo = {
        "log_time": str(datetime.datetime.now()),
        "cap1val": f"{self.getCap1Val()}",
        "cap2val": f"{self.getCap2Val()}",
        "isBattery": f"{self.isBattery()}",
        "isCharging": f"{self.isCharging()}"
            }
        return ioInfo

    def readConf(self):
        fifo_read = open('/tmp/IO_conf', 'r')
        data = json.load(fifo_read)
        self.sendKillSig(data["sendKillSig"])
        self.setBuzzer(data["setBuzzer"])
        self.setSpeaker(data["setSpeaker"])
        self.setBootloader(data["setBootloader"])
        self.setDias(data["setDias"])
        self.setFlash(data["setFlash"])
        fifo_read.close()
        #print(data["battery"]["Alert"])

if __name__ == "__main__":
    import board
    i2c = board.I2C()
    io = IOexpander(i2c)

    io.readConf()