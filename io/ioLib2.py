import gpiod
import time

# sudo apt install python3-libgpiod

class WandIO:
    def __init__(self):
        chip_label0 = 'gpiochip0'
        chip_label2 = 'gpiochip2'

        self.chip0 = gpiod.Chip(chip_label0)
        self.chip2 = gpiod.Chip(chip_label2)

        self.mcp_input_lines = [[0, 2, 4, 6, 7], ["power_stat", "button1", "button2", "power", "power"]]
        self.rpi_input_lines = [[19, 6, 27, 17], ["interrupt", "interrupt", "interrupt", "interrupt"]]
        
        self.mcp_output_lines = [[1, 3, 5], ["cap_rst", "vibmotor", "sound"]] 
        self.rpi_output_lines = [[4, 12, 13], ["bootloader","DIAS", "flash"]]

        self.mcp_gpio_lines = {} 
        self.rpi_gpio_lines = {}

        # Init MCP23008 input GPIO
        for pin_number, consumer in zip(self.mcp_input_lines[0], self.mcp_input_lines[1]):
             self.configure_input(chip_label=2, gpio_list=[pin_number, consumer])

        # Init MCP23008 output GPIO
        for pin_number, consumer in zip(self.mcp_output_lines[0], self.mcp_output_lines[1]):
            self.configure_output(chip_label=2, gpio_list=[pin_number, consumer])



        # Init RPi input GPIO
        for pin_number, consumer in zip(self.rpi_input_lines[0], self.rpi_input_lines[1]):
            self.configure_input(chip_label=0, gpio_list=[pin_number, consumer])

        # Init RPi output GPIO
        for pin_number, consumer in zip(self.rpi_output_lines[0], self.rpi_output_lines[1]):
            self.configure_output(chip_label=0, gpio_list=[pin_number, consumer])
        

    def configure_input(self, chip_label, gpio_list):
        if (chip_label == 0):
            if gpio_list[0] not in self.rpi_gpio_lines:
                gpio_line = self.chip0.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_IN)
                self.rpi_gpio_lines[gpio_list[0]] = gpio_line
                
        elif (chip_label == 2):
            if gpio_list[0] not in self.mcp_gpio_lines:
                gpio_line = self.chip2.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_IN)
                self.mcp_gpio_lines[gpio_list[0]] = gpio_line

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
        if (chip_label == 0):
            if gpio_list[0] not in self.rpi_gpio_lines:
                gpio_line = self.chip0.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_OUT)
                self.rpi_gpio_lines[gpio_list[0]] = gpio_line
        elif (chip_label == 2):
            if gpio_list[0] not in self.mcp_gpio_lines:
                gpio_line = self.chip2.get_line(gpio_list[0])
                gpio_line.request(consumer=gpio_list[1], type=gpiod.LINE_REQ_DIR_OUT)
                self.mcp_gpio_lines[gpio_list[0]] = gpio_line

    def set_output(self, chip_label, pin_number, value):
        if chip_label == "rpi":
            if pin_number in self.rpi_gpio_lines:
                gpio_line = self.rpi_gpio_lines[pin_number]
                if gpio_line.is_requested():
                    gpio_line.set_value(value)
        elif chip_label == "mcp":
            if pin_number in self.rpi_gpio_lines:
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



    def get_button_val(self, button):
        if button == 0:
            return self.read_input("mcp",2)
        elif button == 1:
            return self.read_input("mcp",4)


if __name__ == "__main__":
    wand = WandIO()
    wand.set_output("rpi",12,0)
    time.sleep(1)
    wand.set_output("rpi", 12, 1)
    time.sleep(1)
    wand.set_output("rpi", 12, 0)
    wand.release_all_pins()
