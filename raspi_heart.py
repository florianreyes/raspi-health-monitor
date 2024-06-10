import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(17, GPIO.IN)  # Set GPIO pin 17 as input


def monitor_heartbeat():
    try:
        while True:
            # Check if the sensor sends a high signal
            if GPIO.input(17):
                print("Heartbeat detected")
            else:
                print("No heartbeat detected")
            time.sleep(0.5)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    monitor_heartbeat()


import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(17, GPIO.IN)  # Set GPIO pin 17 as input


def calculate_bpm(timestamps):
    if len(timestamps) < 2:
        return 0
    intervals = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
    avg_interval = sum(intervals) / len(intervals)
    bpm = 60 / avg_interval
    return bpm


def measure_heart_rate(pin, duration):
    timestamps = []
    start_time = time.time()

    print("Measuring heart rate...")

    try:
        while time.time() - start_time < duration:
            if GPIO.input(pin):
                current_time = time.time()
                timestamps.append(current_time)

                # Only keep the last 10 timestamps for BPM calculation
                if len(timestamps) > 10:
                    timestamps.pop(0)
                    bpm = calculate_bpm(timestamps)
                    print(bpm)

                # Debounce - wait until the signal goes low again
                while GPIO.input(pin):
                    time.sleep(0.01)
            time.sleep(0.01)  # Polling interval
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    finally:
        GPIO.cleanup()

    return bpm


# Example usage
if __name__ == "__main__":
    pin = 17  # GPIO pin where the heartbeat sensor is connected
    duration = 30  # Measure heart rate for 30 seconds
    bpm = measure_heart_rate(pin, duration)
    print(f"Heart rate: {bpm:.2f} BPM")
