import time
import board
import busio
import adafruit_ahtx0

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
sensor = adafruit_ahtx0.AHTx0(i2c)

for i in range(2):
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(5)