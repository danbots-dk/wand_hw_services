import os
import time
class SysfsPWM:
    def __init__(self, pwm_chip, pwm_channel):
        self.pwm_chip = pwm_chip
        self.pwm_channel = pwm_channel
        self.base_path = f"/sys/class/pwm/{pwm_chip}/pwm{pwm_channel}/"

        if not os.path.exists(self.base_path):
            self.export_pwm_channel()

    def export_pwm_channel(self):
        pwm_export_path = f"/sys/class/pwm/{self.pwm_chip}/export"
        with open(pwm_export_path, "w") as f:
            f.write(str(self.pwm_channel))

    def set_duty_cycle(self, duty_cycle_percent):
        if duty_cycle_percent < 0 or duty_cycle_percent > 100:
            raise ValueError("Duty cycle percentage must be between 0 and 100.")

        period_ns = int(1e9 / self.get_frequency())  # Convert Hertz to nanoseconds
        duty_cycle_ns = int((duty_cycle_percent / 100) * period_ns)

        with open(os.path.join(self.base_path, "duty_cycle"), "w") as f:
            f.write(str(duty_cycle_ns))

    def pwm_enable(self, enable):
        with open(os.path.join(self.base_path, "enable"), "w") as f:
            f.write(str(enable))

    def set_frequency(self, frequency_hz):
        period_ns = int(1e9 / frequency_hz)  # Convert Hertz to nanoseconds
        with open(os.path.join(self.base_path, "period"), "w") as f:
            f.write(str(period_ns))

    def get_frequency(self):
        period_ns = self.get_period_ns()
        return 1e9 / period_ns  # Convert nanoseconds to Hertz

    def get_period_ns(self):
        with open(os.path.join(self.base_path, "period"), "r") as f:
            period_ns = int(f.read())
        return period_ns
    

if __name__ == "__main__":
    try:
        pwm = SysfsPWM("pwmchip0", 1)  # Change "pwmchip0" and 0 to your specific PWM chip and channel
        pwm.set_frequency(2000)  # Set the PWM frequency in Hertz (e.g., 2000 Hz)
        pwm.pwm_enable(1)
        for i in range(100):
            pwm.set_duty_cycle(i)  # Set the PWM duty cycle as a percentage (e.g., 50%)
            time.sleep(0.01)
        for i in range (100, 0, -1):
            pwm.set_duty_cycle(i)  # Set the PWM duty cycle as a percentage (e.g., 50%)
            time.sleep(0.01)
        pwm.pwm_enable(0)
        # Do other operations with the PWM as needed

    except FileNotFoundError as e:
        print(e)
