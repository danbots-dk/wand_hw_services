from ioLib2 import WandIO
from sysfsPWM import SysfsPWM
import os
from cat24c512 import Eeprom
import datetime

wand = WandIO()
eeprom = Eeprom()
pwm0 = None
pwm1 = None

# sysfsPWM needs x number of tries to initilize
for i in range(3):
    try:
        pwm0 = SysfsPWM("pwmchip0", 0)  # Dias
        if pwm0 != None:
            break
    except:
        pass

# sysfsPWM needs x number of tries to initilize
for i in range(3):
    try:
        pwm1 = SysfsPWM("pwmchip0", 1)  # Dias
        if pwm1 != None:
            break
    except:
        pass

# Brightness is normalized between 0-1. Frequncy is in Hz
def set_dias(brightness, frequency = 2000):
    pwm0.set_frequency(frequency)
    if brightness > 0:
        pwm0.pwm_enable(1)
        pwm0.set_duty_cycle(brightness)
    else:
        pwm0.pwm_enable(0)

# Brightness is normalized between 0-1. Frequncy is in Hz
def set_flash(brightness, frequency = 2000):
    pwm1.set_frequency(frequency)
    if brightness > 0:
        pwm1.pwm_enable(1)
        pwm1.set_duty_cycle(brightness)
    else:
        pwm1.pwm_enable(0)

# Interrupt handler for button1, callback runs in seperate thread 
def set_button1_interrupt(callback):
    wand.configure_interrupt(chip_label="mcp", gpio_list=[2, "button1"], callback=callback)

# Interrupt handler for button2, callback runs in seperate thread 
def set_button2_interrupt(callback):
    wand.configure_interrupt(chip_label="mcp", gpio_list=[3, "button2"], callback=callback)

# Interrupt handler for on/off ic (max16150)
def set_on_off_ic_interrupt(callback):
    wand.configure_interrupt(chip_label="rpi", gpio_list=[27, "on_off_ic"], callback=callback)

# Interrupt handler for on/off button press
# Use set_on_off_ic_interrupt() instead unless you know what you are doing
def set_on_off_button_interrupt(callback):
    wand.configure_interrupt(chip_label="rpi", gpio_list=[26, "on_off_button"], callback=callback)

# Set onboard activity led state
def set_activity_led(on_or_off):
    # 0: Turn activity led off
    # 1: Turn activity led on
    try:
        os.system(f'sudo sh -c "echo {on_or_off} > /sys/class/leds/ACT/brightness"')
    except:
        print("Activity LED failed. You are probably not root.")
        return 0
    
# Set onboard power led state
def set_power_led(on_or_off):
    # 0: Turn power led off
    # 1: Turn power led on
    try:
        os.system(f'sudo sh -c "echo {on_or_off} > /sys/class/leds/PWR/brightness"')
    except:
        print("Activity LED failed. You are probably not root.")
        return 0

# returns the primary power source 
def get_primary_power_source():
    # 0: USB is primary
    # 1: Battery is primary
    return wand.read_input("mcp", 0)

# On next reboot, rpi will enter bootloader mode. 
def enter_boot_loader():
    wand.set_output("rpi", 4, 1)

# Disable 5v boost converter, do not use here unless you know what you are doing!.
def kill_psu():
    #wand.configure_output(chip_label="rpi", gpio_list=[22, "kill_psu"])
    print("kill psu")
    wand.set_output("rpi", 22, 1)

# Set the carrier board version
def eeprom_carrier_brd_version(version):
    eeprom.set_version(version, "carrier")

# Set image install date, can be written more than once with force
def eeprom_img_install_date(force = 0):
    if (eeprom.get_version(eeprom.img_install_date) == 0 or eeprom.get_version(eeprom.img_install_date) != 255) or force == 1:
        current_time = datetime.datetime.now()
        eeprom.set_version(f"{current_time.day}{current_time.month}{current_time.year}", "img_install_date")






    
if __name__ == "__main__":
    import time

    def button1_callback(event):
        print("button1 interrupt")

    def button2_callback(event):
        print("button2 interrupt")

    set_button1_interrupt(button1_callback)
    set_button2_interrupt(button2_callback)
    set_flash(1)
    print(get_primary_power_source())
    kill_psu()
    while(1):
        set_activity_led(1)
        time.sleep(0.1)