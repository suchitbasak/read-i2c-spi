# Link to datasheet: https://asairsensors.com/wp-content/uploads/2021/09/Data-Sheet-AHT20-Humidity-and-Temperature-Sensor-ASAIR-V1.0.03.pdf
import time
import board
import busio

# define I2C device as usual
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

# Lock the I2C device before we try to scan
while not i2c.try_lock():
    pass
# Print the addresses found once
print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])

time.sleep(0.1) # let the sensor initialize
data = bytearray(6)

# soft reset first
i2c.writeto(0x38, bytes([0xBA]))
time.sleep(0.02)


for i in range(1):
# start measurement
    i2c.writeto(0x38, bytes([0xAC, 0x33, 0x00]))
    time.sleep(0.08)


    i2c.readfrom_into(0x38, data)

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

    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")
    time.sleep(2)

i2c.deinit()