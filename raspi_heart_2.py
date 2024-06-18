import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
import time

GAIN = 1
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
