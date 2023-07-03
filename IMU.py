import FaBo9Axis_MPU9250 #or equivalent library
import time
import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()
pos = (0,0)
ux = 0
uy = 0
#need a trigger so that when start is pressed this will begin
try:
    while True:
        position = {
        "position": pos,
        }
        # convert into JSON:
        out = json.dumps(position)
        time.sleep(0.1)
        accel = mpu9250.readAccel()
        ax = accel['x']
        ay = accel['y']
        az = accel['z']
        #to convert values to actual acceleration values?
        #Rx = (AdcRx * Vref / 1023 – VzeroG) / Sensitivity (Eq.2)
        #Ry = (AdcRy * Vref / 1023 – VzeroG) / Sensitivity
        #Rz = (AdcRz * Vref / 1023 – VzeroG) / Sensitivity
        gyro = mpu9250.readGyro()
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']
        vx = ux + ax*0.5
        vy = uy + ay*0.5 
        sx = 0.5*ux + 0.5*0.01*ax
        sy = 0.5*uy + 0.5*0.01*ay
        pos = pos + (sx,sy)#check if this works
        #unsure how to incorporate gyroscope
        #below gives rate of angle change deg/second in xy and yz axis
        #RateAxy = (AdcGyroXY * Vref / 1023 – VzeroRate) / Sensitivity 
        #RateAyz = (AdcGyroYZ * Vref / 1023 – VzeroRate) / Sensitivity
        #http://www.starlino.com/imu_guide.html check website
        
        
    
except KeyboardInterrupt:
    sys.exit()