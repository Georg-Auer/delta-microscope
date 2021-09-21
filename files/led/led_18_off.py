import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
except:
    print("GPIOs already set or unavailable")

# setting blue led to on
GPIO.output(18, GPIO.LOW)
# time.sleep(5)
# GPIO.output(23, GPIO.LOW)
# GPIO.output(24, GPIO.HIGH)
# time.sleep(5)
# GPIO.output(24, GPIO.LOW)
# GPIO.output(25, GPIO.HIGH)
# time.sleep(5)
# GPIO.output(25, GPIO.LOW)

# GPIO.output(23, GPIO.LOW)
# GPIO.output(24, GPIO.LOW)
# GPIO.output(25, GPIO.LOW)
