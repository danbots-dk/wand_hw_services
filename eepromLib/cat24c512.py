import qwiic_eeprom
import time
import sys

# board versions
# - Carrier = 0
# - Front touch = 10
# - On/Off = 20
# - FlashFlex = 30

# image version 
# - Version = 40
# - Installation date = 50

# lib versions
# - io = 60
# - battery = 70
# - imu = 80
# - eeprom = 90

eeprom_idx = {"carrier": 0,
            "front_touch": 10,
            "on_off": 20,
            "flash_flex": 30,
            "img_version": 40,
            "img_install_date": 50,
            "io_service": 60,
            "battery_service": 70,
            "imu_service": 80,
            "eeprom": 90
             }


class Eeprom():
    def __init__(self):
        self.eeprom = qwiic_eeprom.QwiicEEPROM(0x50)

        if self.eeprom.begin() != True:
            print("\nEeprom not found. Please check your connection or adress", \
                file=sys.stderr)
            

    def str2bytes(self, string):
        bytes_data = string.encode('utf-8')
        num_bytes_used = len(bytes_data)
        return bytes_data

    def write_bytes(self, string, idx):
        bytes_data = self.str2bytes(string)

        for i in range(10):
            self.eeprom.write_byte(i+idx, 0x03)

        for i, byte in enumerate(bytes_data):
            self.eeprom.write_byte(i+idx, byte)

    def get_bytes(self, idx):
        eeprom_read = ""
        for i in range(10):
            eeprom_read += chr(self.eeprom.read_byte(i+idx))

        return eeprom_read


    def set_version(self, val, idx):
        idx = eeprom_idx[idx]
        self.carrier_version = val
        self.write_bytes(val, idx)
        return 1

    def get_version(self, idx):
        return self.get_bytes(eeprom_idx[idx])

    def get_all_version(self):
        versions = ""
        for idx in eeprom_idx:
            versions += f"{idx}: {self.get_version(idx)} \n"
        return versions


if __name__ == "__main__":
    eeprom = Eeprom()
    eeprom.set_version("04092023", "img_install_date")

    #print(eeprom.get_version(eeprom_idx["img_install_date"]))
    print(eeprom.get_all_version())

    #bytes_data, bytes_len = eeprom.str2bytes("test")
    #print(f"{(bytes_data[0])} - {bytes_len}")



