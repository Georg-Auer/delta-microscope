import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
except:
    print("GPIOs already set or unavailable")
# GPIO.output(23, GPIO.HIGH)
# GPIO.output(24, GPIO.HIGH)
# GPIO.output(25, GPIO.HIGH)

GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)
