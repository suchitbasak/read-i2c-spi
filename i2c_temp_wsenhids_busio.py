import time
import board
import busio

# Define I2C device
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

while not i2c.try_lock():
    pass

# Print the addresses found once
print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])


# WSEN-HIDS I2C address
HIDS_I2C_ADDRESS = 0x44

# Command to start measurement (continuous mode)
START_MEASUREMENT = [0xE0]

# Function to read data from the sensor
def read_hids_data():
    data = bytearray(6)

    # Trigger measurement
    i2c.writeto(HIDS_I2C_ADDRESS, bytes(START_MEASUREMENT))
    time.sleep(0.1)  # Wait for measurement to complete

    # Read 6 bytes of data
    i2c.readfrom_into(HIDS_I2C_ADDRESS, data)
    
    return data

# Function to calculate humidity and temperature from raw data
def calculate_humidity_temperature(data):
    srh = (data[3] << 8) | data[4]
    humidity = -6.0 + ((125.0 * srh)/(65536-1))
    
    st = (data[0] << 8) | data[1];
    temperature = -45.0 + ((175.0 * st)/(65536-1));
    return humidity, temperature

# Main loop to read and print data
for i in range(1):
    data = read_hids_data()
    humidity, temperature = calculate_humidity_temperature(data)

    print(f"Humidity: {humidity:.2f}%")
    print(f"Temperature: {temperature:.2f}°C")
    
    time.sleep(1)
