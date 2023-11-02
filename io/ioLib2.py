import gpiod
import time
import threading
import os

# sudo apt install python3-libgpiod

class WandIO:
    def __init__(self):
        chip_label0 = 'gpiochip0'
        chip_label2 = 'gpiochip2'

        self.chip0 = gpiod.Chip(chip_label0)
        self.chip2 = gpiod.Chip(chip_label2)

        self.mcp_input_lines = [[0, 6, 7], ["power_stat", "power", "power"]]
        self.rpi_input_lines = [[], []]
        
        self.mcp_output_lines = [[1, 4, 5], ["cap_rst", "mirror_heat", "sound"]] 
        self.rpi_output_lines = [[4, 12, 13, 22], ["bootloader","DIAS", "flash" "kill"]]

        self.mcp_interrupt_lines = [[2, 3], ["button1", "button2"]]
        self.rpi_interrupt_lines = [[27, 6, 17], ["on_off_interrupt", "carrier_pcb_temp", "battert_fuel_interrupt"]]

        self.mcp_gpio_lines = {} 
        self.rpi_gpio_lines = {}

        # Configure MCP23008 input GPIO
        for pin_number, consumer in zip(self.mcp_input_lines[0], self.mcp_input_lines[1]):
             self.configure_input(chip_label="mcp", gpio_list=[pin_number, consumer])

        # Configure MCP23008 output GPIO
        for pin_number, consumer in zip(self.mcp_output_lines[0], self.mcp_output_lines[1]):
            self.configure_output(chip_label="mcp", gpio_list=[pin_number, consumer])



        # Configure RPi input GPIO
        for pin_number, consumer in zip(self.rpi_input_lines[0], self.rpi_input_lines[1]):
            self.configure_input(chip_label="rpi", gpio_list=[pin_number, consumer])

        # Configure RPi output GPIO
        for pin_number, consumer in zip(self.rpi_output_lines[0], self.rpi_output_lines[1]):
            self.configure_output(chip_label="rpi", gpio_list=[pin_number, consumer])



        # Configure MCP23008 interrupt GPIO
        #for pin_number, consumer in zip(self.mcp_interrupt_lines[0], self.mcp_interrupt_lines[1]):
        #     self.configure_interrupt(chip_label="mcp", gpio_list=[pin_number, consumer], name=consumer)

        # Configure RPi interrupt GPIO
        #for pin_number, consumer in zip(self.rpi_interrupt_lines[0], self.rpi_interrupt_lines[1]):
        #     self.configure_interrupt(chip_label="rpi", gpio_list=[pin_number, consumer], name=consumer)
        

    def configure_input(self, chip_label, gpio_list):
        if (chip_label == "rpi"):
            if gpio_list[0] not in self.rpi_gpio_lines:
                gpio_line = self.chip0.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_IN)
                self.rpi_gpio_lines[gpio_list[0]] = gpio_line
            else:
                print(f"Cannot configure input on {chip_label} pin {gpio_list[0]}. Is there an existing configuration on the same pins elsewhere?")
                return 0
                
        elif (chip_label == "mcp"):
            if gpio_list[0] not in self.mcp_gpio_lines:
                gpio_line = self.chip2.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_IN)
                self.mcp_gpio_lines[gpio_list[0]] = gpio_line
            else:
                print(f"Cannot configure input on {chip_label} pin {gpio_list[0]}. Is there an existing configuration on the same pins elsewhere?")
                return 0

    def read_input(self, chip_label, pin_number):
            if chip_label == "rpi":
                if pin_number in self.rpi_gpio_lines:
                    gpio_line = self.rpi_gpio_lines[pin_number]
                    if gpio_line.is_requested():
                        return gpio_line.get_value()
            elif chip_label == "mcp":
                if pin_number in self.mcp_gpio_lines:
                    gpio_line = self.mcp_gpio_lines[pin_number]
                    if gpio_line.is_requested():
                        return gpio_line.get_value()
            return None  # Return None if the GPIO line is not fo
    
    def configure_output(self, chip_label, gpio_list):
        if (chip_label == "rpi"):
            if gpio_list[0] not in self.rpi_gpio_lines:
                gpio_line = self.chip0.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_OUT)
                self.rpi_gpio_lines[gpio_list[0]] = gpio_line
            else:
                print(f"Cannot configure output on {chip_label} pin {gpio_list[0]}. Is there an existing configuration on the same pins elsewhere?")
                return 0
        elif (chip_label == "mcp"):
            if gpio_list[0] not in self.mcp_gpio_lines:
                gpio_line = self.chip2.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_OUT)
                self.mcp_gpio_lines[gpio_list[0]] = gpio_line
            else:
                print(f"Cannot configure output on {chip_label} pin {gpio_list[0]}. Is there an existing configuration on the same pins elsewhere?")
                return 0

    def set_output(self, chip_label, pin_number, value):
        if chip_label == "rpi":
            if pin_number in self.rpi_gpio_lines:
                gpio_line = self.rpi_gpio_lines[pin_number]
                if gpio_line.is_requested():
                    gpio_line.set_value(value)
        elif chip_label == "mcp":
            if pin_number in self.mcp_gpio_lines:
                gpio_line = self.mcp_gpio_lines[pin_number]
                if gpio_line.is_requested():
                    gpio_line.set_value(value)

    def release_pin(self, chip_label, pin_number):
        if chip_label == "rpi":
            if pin_number in self.rpi_gpio_lines:
                gpio_line = self.rpi_gpio_lines.pop(pin_number)
                gpio_line.release()
        elif chip_label == "mcp":
            if pin_number in self.mcp_gpio_lines:
                gpio_line = self.mcp_gpio_lines.pop(pin_number)
                gpio_line.release()

    def release_all_pins(self):
        # Release all RPi GPIO pins
        rpi_keys = list(self.rpi_gpio_lines.keys())  # Create a list of keys
        for pin_number in rpi_keys:
            gpio_line = self.rpi_gpio_lines.pop(pin_number)
            gpio_line.release()
            # configure as output to avoid leakage (high impedance)?
            # gpio_line.request(consumer="input", type=gpiod.LINE_REQ_DIR_IN)  # Configure as input

        # Release all MCP23008 GPIO pins
        mcp_keys = list(self.mcp_gpio_lines.keys())
        for pin_number in mcp_keys:
            gpio_line = self.mcp_gpio_lines.pop(pin_number)
            gpio_line.release()
            # configure as output to avoid leakage (high impedance)?
            # gpio_line.request(consumer="input", type=gpiod.LINE_REQ_DIR_IN)  # Configure as input

    def configure_interrupt(self, chip_label, gpio_list, debounce = 0.1, callback=None):
        if callback == None:
            return 0
        if chip_label == "mcp" and gpio_list[0] not in self.mcp_gpio_lines:
            gpio_line = self.chip2.get_line(gpio_list[0])
            gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_EV_RISING_EDGE)
            self.mcp_gpio_lines[gpio_list[0]] = gpio_line
        elif chip_label == "rpi" and gpio_list[0] not in self.rpi_gpio_lines:
            gpio_line = self.chip0.get_line(gpio_list[0])
            gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_EV_RISING_EDGE)
            self.rpi_gpio_lines[gpio_list[0]] = gpio_line
        else:
            print(f"Cannot create interrupt on {chip_label} pin {gpio_list[0]}. Is there an existing interrupt on the same pins elsewhere?")
            return 0
            
        def interrupt_thread():
            while True: # loop in case event_wait() times out
                event = gpio_line.event_wait(10000)
                if event:
                    gpio_line.event_read() # release interrupt
                    callback(event)
                    
                    
                    # interrupt_hold_time = 0
                    # interrupt_hold_time_threshold = 3
                    intterupt_hold_delay = 0.05
                    # Wait for the button to be released (polling)
                    while gpio_line.get_value() == 1:                        
                        time.sleep(intterupt_hold_delay)
                        # interrupt_hold_time = interrupt_hold_time + intterupt_hold_delay
                        # print(interrupt_hold_time)
                        # if (interrupt_hold_time > interrupt_hold_time_threshold):
                        #     os.system("shutdown now")
                        #   # Turn off, vibrate etc.
                    
                    # Pop the pin from the appropriate dictionary
                    if chip_label == "mcp" and gpio_list[0] in self.mcp_gpio_lines:
                        self.mcp_gpio_lines.pop(gpio_list[0])
                    elif chip_label == "rpi" and gpio_list[0] in self.rpi_gpio_lines:
                        self.rpi_gpio_lines.pop(gpio_list[0])

                    gpio_line.release()
                    time.sleep(debounce) # acts as a debounce
                    self.configure_interrupt(chip_label, gpio_list, debounce, callback)
                    break
        thread = threading.Thread(target=interrupt_thread)
        thread.daemon = True
        thread.start()
        
    def get_primary_power_source(self):
        # 0: USB is primary
        # 1: Battery is primary
        return self.read_input("mcp",0)
        
def test_interrupt(event):
    print("test interrupt")

def test_interrupt2(event):
    print("test2 interrupt")


if __name__ == "__main__":
    wand = WandIO()
    int1 = wand.configure_interrupt(chip_label="mcp", gpio_list=[3, "button2"], callback=test_interrupt)
    int2 = wand.configure_interrupt(chip_label="mcp", gpio_list=[2, "button1"], callback=test_interrupt2)
    wand.release_pin("mcp", 7)
    #wand.set_output("mcp",5,0)
    while(1):
        try:
            #print(wand.get_primary_power_source())
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Releasing all pins")
            wand.release_all_pins()
            break
        

 
