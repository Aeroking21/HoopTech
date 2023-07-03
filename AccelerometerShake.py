import time
import board
import digitalio
import adafruit_lis3dh
from time import sleep
import math
import json
i2c = board.I2C()
int1 = digitalio.DigitalInOut(board.D4)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)


while True:
    shake_accel = (0,0,0)
    for _ in range (10):
        shake_accel = tuple(map(sum, zip(shake_accel, lis3dh.acceleration)))
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
