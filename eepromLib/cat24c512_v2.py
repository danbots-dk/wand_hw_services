import smbus2

# Define the I2C bus and EEPROM address
bus_number = 1  # Use the appropriate I2C bus number
eeprom_address = 0x50  # Replace with your EEPROM's I2C address

# Initialize the I2C bus
bus = smbus2.SMBus(bus_number)

# Define the EEPROM size
eeprom_size = 65536  # Size of the AT24C512 in bytes

# Define an EEPROM memory address to read/write data
eeprom_memory_address = 0x0000  # Change this address as needed

# Read data from the EEPROM
def read_eeprom():
    try:
        data = bus.read_i2c_block_data(eeprom_address, eeprom_memory_address, 32)
        print("Data read from EEPROM:", data)
    except Exception as e:
        print("Error reading from EEPROM:", str(e))

# Write data to the EEPROM
def write_eeprom(data):
    try:
        data_to_write = [eeprom_memory_address] + data
        bus.write_i2c_block_data(eeprom_address, eeprom_memory_address, data_to_write)
        print("Data written to EEPROM")
    except Exception as e:
        print("Error writing to EEPROM:", str(e))

# Clear the entire EEPROM by writing zeros (0x00) to every address
def clear_eeprom():
    data_to_clear = [0x00] * eeprom_size
    write_eeprom(data_to_clear)
    print("EEPROM cleared")

if __name__ == "__main__":
    # Clear the EEPROM
    clear_eeprom()
    read_eeprom()

    # Example data to write (replace with your own data)
    data_to_write = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

    # Write data to the EEPROM
    write_eeprom(data_to_write)
    read_eeprom()
