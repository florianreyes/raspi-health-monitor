# import RPi.GPIO as GPIO
# import time
# # Setup
# GPIO.setmode(GPIO.BCM)  # Use BCM numbering
# GPIO.setup(17, GPIO.IN)  # Set GPIO pin 17 as input

# def monitor_heartbeat():
#     try:
#         while True:
#             # Check if the sensor sends a high signal
#             if GPIO.input(17):
#                 print("Heartbeat detected")
#             else:
#                 print("No heartbeat detected")
#             time.sleep(0.5)  # Adjust the delay as needed
#     except KeyboardInterrupt:
#         print("Monitoring stopped by user")
#     finally:
#         GPIO.cleanup()


# if __name__ == "__main__":
#     monitor_heartbeat()


# import RPi.GPIO as GPIO
# import time

# # Setup
# GPIO.setmode(GPIO.BCM)  # Use BCM numbering
# GPIO.setup(17, GPIO.IN)  # Set GPIO pin 17 as input


# def calculate_bpm(timestamps):
#     if len(timestamps) < 2:
#         return 0
#     intervals = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
#     avg_interval = sum(intervals) / len(intervals)
#     bpm = 60 / avg_interval
#     return bpm


# def measure_heart_rate(pin, duration):
#     timestamps = []
#     start_time = time.time()

#     print("Measuring heart rate...")

#     try:
#         while time.time() - start_time < duration:
#             if GPIO.input(pin):
#                 current_time = time.time()
#                 timestamps.append(current_time)

#                 # Only keep the last 10 timestamps for BPM calculation
#                 if len(timestamps) > 10:
#                     timestamps.pop(0)
#                     bpm = calculate_bpm(timestamps)
#                     print(bpm)

#                 # Debounce - wait until the signal goes low again
#                 while GPIO.input(pin):
#                     time.sleep(0.01)
#             time.sleep(0.01)  # Polling interval
#     except KeyboardInterrupt:
#         print("Monitoring stopped by user")
#     finally:
#         GPIO.cleanup()

#     return bpm


# # Example usage
# if __name__ == "__main__":
#     pin = 17  # GPIO pin where the heartbeat sensor is connected
#     duration = 30  # Measure heart rate for 30 seconds
#     bpm = measure_heart_rate(pin, duration)
#     print(f"Heart rate: {bpm:.2f} BPM")

# import time
# import Adafruit_ADS1x15
# import Adafruit_GPIO.SPI as SPI
# import serial

# GAIN = 2 / 3
# rate = [0] * 10
# amp = 100


# def read_pulse():
#     firstBeat = True
#     secondBeat = False
#     samplecounter = 0
#     lastBeatTime = 0
#     lastTime = int(time.time() * 1000)
#     th = 525
#     P = 512
#     T = 512
#     IBI = 600
#     pulse = False
#     adc = Adafruit_ADS1x15.ADS1015()
#     adc.start_adc(0, gain=GAIN)
#     while True:
#         signal = adc.read_adc(0, gain=GAIN)
#         curTime = int(time.time() * 1000)
#         samplecounter += curTime - lastTime
#         lastTime = curTime
#         N = samplecounter - lastBeatTime
#         if signal < th and N > (IBI / 5.0) * 3.0:
#             if signal < T:
#                 T = signal
#         if N > 250:
#             if (signal > th) and (Pulse == False) and (N > (IBI / 5.0) * 3.0):
#                 Pulse = 1
#                 IBI = samplecounter - lastBeatTime
#                 lastBeatTime = samplecounter
#                 if secondBeat:
#                     secondBeat = 0
#                     for i in range(0, 10):
#                         rate[i] = IBI
#                 if firstBeat:
#                     firstBeat = 0
#                     secondBeat = 1
#                     continue
#                 runningTotal = 0
#                 for i in range(0, 9):
#                     rate[i] = rate[i + 1]
#                     runningTotal += rate[i]
#                 rate[9] = IBI
#                 runningTotal += rate[9]
#                 runningTotal /= 10
#                 BPM = 60000 / runningTotal
#                 print("BPM:" + str(BPM))

#         if signal < th and pulse == 1:
#             amp = P - T
#             th = amp / 2 + T
#             T = th
#             P = th
#             pulse = 0
#         if N > 2500:
#             th = 512
#             T = th
#             P = th
#             lastBeatTime = samplecounter
#             firstBeat = 0
#             secondBeat = 0
#             print("no beats found")
#         time.sleep(0.005)


# read_pulse()

import time
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio

GAIN = 2 / 3
rate = [0] * 10
amp = 100


def read_pulse():
    firstBeat = True
    secondBeat = False
    samplecounter = 0
    lastBeatTime = 0
    lastTime = int(time.time() * 1000)
    th = 525
    P = 512
    T = 512
    IBI = 600
    pulse = False

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1015(i2c)

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)

    while True:
        signal = chan.value
        curTime = int(time.time() * 1000)
        samplecounter += curTime - lastTime
        lastTime = curTime
        N = samplecounter - lastBeatTime
        if signal < th and N > (IBI / 5.0) * 3.0:
            if signal < T:
                T = signal
        if N > 250:
            if (signal > th) and (pulse == False) and (N > (IBI / 5.0) * 3.0):
                pulse = 1
                IBI = samplecounter - lastBeatTime
                lastBeatTime = samplecounter
                if secondBeat:
                    secondBeat = 0
                    for i in range(0, 10):
                        rate[i] = IBI
                if firstBeat:
                    firstBeat = 0
                    secondBeat = 1
                    continue
                runningTotal = 0
                for i in range(0, 9):
                    rate[i] = rate[i + 1]
                    runningTotal += rate[i]
                rate[9] = IBI
                runningTotal += rate[9]
                runningTotal /= 10
                BPM = 60000 / runningTotal
                print("BPM:" + str(BPM))

        if signal < th and pulse == 1:
            amp = P - T
            th = amp / 2 + T
            T = th
            P = th
            pulse = 0
        if N > 2500:
            th = 512
            T = th
            P = th
            lastBeatTime = samplecounter
            firstBeat = 0
            secondBeat = 0
            print("no beats found")
        time.sleep(0.005)


read_pulse()
