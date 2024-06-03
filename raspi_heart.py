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
