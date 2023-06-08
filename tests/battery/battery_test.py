"""
Battery tests
This module contain test of battery user interfaces
"""

#   230608  PLH     First template

_DEBUG = True

def get_battery_info():
    "return the information from battery"
    if _DEBUG:
        print("Getting the information from battery")
    voltage = 3.4799
    percent = 0.1123
    power = False
    rest_time = 62.7 # minutes


    return voltage, percent, power, rest_time


if __name__ == '__main__':
    vol, per, chg, rest = get_battery_info()

    print(f"Voltage: {vol:2.2f}V, Charge {per*100:.0f}% Rest time: {rest:3.0f} min, Charging: {chg}")
