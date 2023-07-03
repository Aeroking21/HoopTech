# [HoopTech](https://aleeraewan.wixsite.com/baller)


<img src="screenshot.png" alt="alt text" style="width:250px;height:250px; border-radius:50%; margin-left:200px">

Introducing a personal basketball trainer that motivates your dribbling and movement. Fine Tune Your Routine With Precise Workout Stats
HoopTech is a two part device designed to track your basketball training to optimize your performance! With state-of-the-art sensors, the app monitors your calories burnt, speed, and number of successful shots. One part of sensors is wrapped on the user, while the other is secured to the rim of the basketball hoop. 

Track the number of shots you score in each training session, along with each one's accuracy. The second half of our device is placed on the rim of the basketball hoop and uses a proximity sensor to count the number of successful shots, while an accelerometer measures the size of the vibration on the basketball hoop.
The cleaner your shot, the higher your accuracy score.
With this device you can also view past training sessions and monitor progress!


Monitor the number of calories you burn as you practise your dribbling and lay-ups! The device uses a pulse-rate sensor to calculate approximate calories burnt from your heart rate as you run around on the court.

The device connected to the player includes an accelerometer which records your maximum acceleration on the court. Monitor your fastest accelerations to best improve your training routine for maximising progress!

## Sensors used and its respective library file:

- the pulse sensor along with ADC (ADS1115) module - `ads1115.py`
- accelerometer (LIS3DH) - `lis3dh.py`
- time-of-flight (VL53L0X) ranging sensor - `VL53L0X.py`

A buzzer (GPIO 10) and LED (GPIO 27) as outputs to indicate that the baskets have been made.

All libraries have been implemented by using the I2C functions in the `smbus2`.

## Handling multiple tasks concurrently

- **Threading** was implemented to collect data at different rates with the 3 different sensors.
- 4 main tasks:
  - Measure pulse rate
  - Track score
  - Track maximum acceleration
  - Send data over MQTT (every 1s)


## Directory structure

```

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

