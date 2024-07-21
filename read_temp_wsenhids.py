import time
import board
import busio

# Define I2C device
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)

# WSEN-HIDS I2C address
HIDS_I2C_ADDRESS = 0x5F

# Command to start measurement (continuous mode)
START_MEASUREMENT = [0xAC, 0x33, 0x00]

# Function to read data from the sensor
def read_hids_data():
    data = bytearray(6)

    # Trigger measurement
    i2c.writeto(HIDS_I2C_ADDRESS, bytes(START_MEASUREMENT))
    time.sleep(0.08)  # Wait for measurement to complete

    # Read 6 bytes of data
    i2c.readfrom_into(HIDS_I2C_ADDRESS, data)
    
    return data

# Function to calculate humidity and temperature from raw data
def calculate_humidity_temperature(data):
    # Humidity calculation
    h = data[1]
    h <<= 8
    h |= data[2]
    h <<= 4
    h |= data[3] >> 4
    humidity = (float(h) * 100) / 0x100000

    # Temperature calculation
    tdata = data[3] & 0x0F
    tdata <<= 8
    tdata |= data[4]
    tdata <<= 8
    tdata |= data[5]
    temperature = (float(tdata) * 200 / 0x100000) - 50

    return humidity, temperature

# Main loop to read and print data
while True:
    data = read_hids_data()
    humidity, temperature = calculate_humidity_temperature(data)

    print(f"Humidity: {humidity:.2f}%")
    print(f"Temperature: {temperature:.2f}°C")
    
    time.sleep(1)
