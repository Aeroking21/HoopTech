import time
import board
import digitalio
import adafruit_lis3dh
from time import sleep
import math
import json
import smbus2
#i2c = board.I2C()
#int1 = digitalio.DigitalInOut(board.D4)  # Set this to the correct pin for the interrupt!
#lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

bus = smbus2.SMBus(1)

LIS3DH_ADDRESS = 0x18

OUT_X_L_REGISTER = 0x28
OUT_X_H_REGISTER = 0x29
OUT_Y_L_REGISTER = 0x2A
OUT_Y_H_REGISTER = 0x2B
OUT_Z_L_REGISTER = 0x2C
OUT_Z_H_REGISTER = 0x2D


while True:
    x_l = bus.read_byte_data(LIS3DH_ADDRESS, OUT_X_L_REGISTER)
    x_h = bus.read_byte_data(LIS3DH_ADDRESS, OUT_X_H_REGISTER)
    y_l = bus.read_byte_data(LIS3DH_ADDRESS, OUT_Y_L_REGISTER)
    y_h = bus.read_byte_data(LIS3DH_ADDRESS, OUT_Y_H_REGISTER)
    z_l = bus.read_byte_data(LIS3DH_ADDRESS, OUT_Z_L_REGISTER)
    z_h = bus.read_byte_data(LIS3DH_ADDRESS, OUT_Z_H_REGISTER)
    #acceleration in x, y, z axis


    
    shake_accel = (0,0,0)
    for _ in range (10):
        x = int.from_bytes(x_l + x_h)
        y = int.from_bytes(y_l + y_h)
        z = int.from_bytes(z_l + z_h)
        acceleration = (x,y,z)
        shake_accel = tuple(map(sum, zip(shake_accel, acceleration)))
        time.sleep(0.1/10)
    avg = tuple(value/10 for value in shake_accel)
    total_accel = math.sqrt(sum(map(lambda x: x * x, avg)))

    if total_accel > 10:
        if total_accel < 20:
            print("Accuracy B")
            x = {
                "accuracy" : "B"
            }

        else:
            print("Accuracy C")
            x = {
                "accuracy" : "C"
            }
        y = json.dumps(x)
    
    

    #accuracy A is when there is no vibration - clean shot
    #change thresholds via testing 
    #change code when removing library (this is heavily based on code for shake library code)
