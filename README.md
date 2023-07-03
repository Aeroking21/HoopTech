# Code (Hardware)

## Sensors used and its respective library file:

- the pulse sensor along with ADC (ADS1115) module - `ads1115.py`
- accelerometer (LIS3DH) - `lis3dh.py`
- time-of-flight (VL53L0X) ranging sensor - `VL53L0X.py`

A buzzer (GPIO 10) and LED (GPIO 27) as outputs to indicate that the baskets have been made.

All libraries have been implemented by using the I2C functions in the `smbus2` library as instructed.

<br>

---

<br>

## Handling multiple tasks concurrently

- **Threading** was implemented to collect data at different rates with the 3 different sensors.
- 4 main tasks:
  - Measure pulse rate
  - Track score
  - Track maximum acceleration
  - Send data over MQTT (every 1s)

<br>

---

<br>

## Directory structure

```
fsf20/hw branch
│
|--README.md
|
|--main.py              -> final code
|
|--ads1115.py           -> adc module library for pulse sensor
|--lis3dh.py            -> accelerometer library
|--VL53L0X.py           -> time-of-flight sensor library
|
|--pulse.py             -> test code for pulse
|--distanceTest.py      -> test code for time-of-flight sensor
|--sound.py             -> test code for buzzer
```

## Accelerometer Code

- Commented out code def shakeCode() is the code to measure the vibrations of the basketball rim
- Measures the average acceleration in specified time frame
- Compares this to two thresholds to determine whether there is a lot or a little shaking and then defines the accuracy as A, B, or C (where A is no vibration)
=======

