import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)

frequency = 150 # Hz
period = 1.0 / frequency
duty_cycle = 0.5
high_time = period * duty_cycle
low_time = period * (1.0 - duty_cycle)

while True:
    
    GPIO.output(10, GPIO.HIGH)
    time.sleep(high_time)
    GPIO.output(10, GPIO.LOW)
    time.sleep(low_time)