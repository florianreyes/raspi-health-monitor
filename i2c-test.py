import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)  # Adjust frequency as needed

# Create the ADS1015 ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 1
chan = AnalogIn(ads, ADS.P0)

# Read and print the ADC values
while True:
    print("Channel 1:", chan.value, "V")
    time.sleep(1)
