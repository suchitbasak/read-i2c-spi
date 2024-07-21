import time
import board
import busio

# Initialize I2C
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

# Lock the I2C device before scanning
while not i2c.try_lock():
    pass

# Print the addresses found once
print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])

time.sleep(0.01)
data = bytearray(6)

# Initialization sequence for AHT20 sensor
# Soft reset command
i2c.writeto(0x38, bytes([0xBA]))
time.sleep(0.02)

# Start measurement command
i2c.writeto(0x38, bytes([0xAC, 0x33, 0x00]))
time.sleep(0.08)

# Read sensor data
for i in range(5):
    # Trigger measurement
    i2c.writeto(0x38, bytes([0xAC, 0x33, 0x00]))
    time.sleep(0.08)

    # Read data into bytearray
    i2c.readfrom_into(0x38, data)
    print("Raw data:", data)
    
    # Check if sensor status bit is ready
    if data[0] & 0x80 == 0:  # Status bit is the highest bit of the first byte
        # Humidity calculation
        h = data[1]
        h <<= 8
        h |= data[2]
        h <<= 4
        h |= data[3] >> 4
        _humidity = (float(h) * 100) / 0x100000

        # Temperature calculation
        tdata = data[3] & 0x0F
        tdata <<= 8
        tdata |= data[4]
        tdata <<= 8
        tdata |= data[5]
        _temperature = (float(tdata) * 200 / 0x100000) - 50

        print(f"Humidity: {_humidity}%")
        print(f"Temperature: {_temperature}°C")
    else:
        print("Sensor not ready, retrying...")

    time.sleep(1)

i2c.unlock()
