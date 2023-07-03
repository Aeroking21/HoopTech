import time
import paho.mqtt.client as mqtt
import json
from time import sleep

import VL53L0X
import ads1115
import lis3dh

import RPi.GPIO as GPIO

import math
import threading

#----------------------------------------------------------------------------------------
# Setup

start = False

tof = VL53L0X.VL53L0X()
adc = ads1115.ADS1115()
sensor = lis3dh.LIS3DH(debug=True)
sensor.setRange(sensor.RANGE_2G)

# Set GPIOs (buzzer & LED) to output mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Generate PWM and set pitch for buzzer
frequency = 150
period = 1.0 / frequency
duty_cycle = 0.5
high_time = period * duty_cycle
low_time = period * (1.0 - duty_cycle)

score = 0
pastScore = 0
maxA = 0

#-----------------------------------------------------------------------------------------

def accelerometer():

	global start
	global maxA

	# for printing purposes
	i = 0
	
	while start:

		x = sensor.getX()
		y = sensor.getY()
		z = sensor.getZ()

		accelerate = pow(pow(x,2) + pow(y,2), 0.5)   
		
		if i % 100 == 0:
			print("a", accelerate, "maxA", maxA)

		if (accelerate > maxA):
			maxA = accelerate
			
		i += 1
		time.sleep(0.01)

# def shakeCode():					# comment this out for raspberry pi on player
    
# 	shake_accel = (0,0,0)
 
# 	x = sensor.getX()
# 	y = sensor.getY()
# 	z = sensor.getZ()
 
# 	for _ in range (10):
# 		acceleration = (x, y, z)
# 		shake_accel = tuple(map(sum, zip(shake_accel, acceleration)))
# 		time.sleep(0.1/10)
  
# 	avg = tuple(value/10 for value in shake_accel)
# 	total_accel = math.sqrt(sum(map(lambda x: x * x, avg)))
# 	#print("total_accel")
# 	#print(total_accel)
 
# 	if total_accel > 10:
     
# 		if total_accel < 20:
      
# 			print("Accuracy B")
# 			shake = {"accuracy" : "B"}

# 		else:
# 			print("Accuracy C")
# 			shake = {"accuracy" : "C"}
   
# 		MSG_INFO = client.publish("shakeAccuracy", json.dumps(shake))
# 		mqtt.error_string(MSG_INFO.rc)
# 		print("shakeAccuracy published:", json.dumps(shake))			

# 	i += 1
# 	time.sleep(0.01)
# # accuracy A is when there is no vibration - clean shot
# # change thresholds via testing 

def scoreDetector():

	global start
	global score
	global pastScore

	print("Score Detector started")
	
	print("Initial Score: ", score)
	
	# Start ranging
	tof.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)

	#VL53L0X_GOOD_ACCURACY_MODE   # Good Accuracy mode
	#VL53L0X_BETTER_ACCURACY_MODE   # Better Accuracy mode
	#VL53L0X_BEST_ACCURACY_MODE   # Best Accuracy mode
	#VL53L0X_LONG_RANGE_MODE   # Longe Range mode
	#VL53L0X_HIGH_SPEED_MODE   # High Speed mode

	timing = 0.02

	# Calibrate diameter of hoop and set the boundary of which ball is detected
	avg_distance = tof.calibrate(timing, tof.get_distance())
	boundary = avg_distance*0.7

	while (start):

		# Detect if basket made 
		distance = tof.get_distance()
		score = tof.detect(distance, boundary, score)

		Data = {
			"bpm": BPM,  
			"score": score
		}

		if (score > pastScore):

			print("Score : ", score)

			buzzerStartTime = time.time();

			while (time.time() - buzzerStartTime < 0.2):
				GPIO.output(27, GPIO.HIGH)
				GPIO.output(10, GPIO.HIGH)
				time.sleep(high_time)
				GPIO.output(10, GPIO.LOW)
				time.sleep(low_time)

			GPIO.output(27, GPIO.LOW)
			time.sleep(0.5)

		pastScore = score

		time.sleep(timing)

	tof.stop_ranging()
	print("Score Detector finished")

BPM = 0
pastBPM = 0

def pulseDetector():

	print("Pulse Detector started")

	global start
	
	GAIN = 2/3  
	curState = 0
	thresh = 525  # mid point in the waveform
	P = 512
	T = 512
	lastBeatTime = 0
	firstBeat = True
	secondBeat = False
	Pulse = False
	IBI = 600
	rate = [0]*10
	amp = 100
	sampleCounter = 0

	global BPM
	global pastBPM
	
	lastTime = int(time.time()*1000)
	lastS = int(time.time())

	while (True):

		# Read from the ADC A0 channel
		Signal = adc.read_adc(0, gain=GAIN)   
		curTime = int(time.time()*1000)

		sampleCounter += curTime - lastTime;          # Keep track of the time in mS
		lastTime = curTime
		N = sampleCounter - lastBeatTime;             # Monitor the time since the last beat to avoid noise

		# Find the peak and trough of the pulse wave
		if Signal < thresh and N > (IBI/5.0)*3.0 :    # Avoid dichrotic noise by waiting 3/5 of last IBI
			if Signal < T :                             # T is the trough
				T = Signal;                                

		if Signal > thresh and  Signal > P:           # P is the peak
			P = Signal;                                 
		
		# Avoid high frequency noise and find 2 consecutive beats
		if N > 250 :                                  
			if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :     

				Pulse = True;                             
				IBI = sampleCounter - lastBeatTime;       
				lastBeatTime = sampleCounter;             

				if secondBeat :                           
					secondBeat = False;                   
					for i in range(0,10):                
						rate[i] = IBI;                      
	
				# Discard if IBI value is unreliable
				if firstBeat :                            
					firstBeat = False;                    
					secondBeat = True;                    
																								
				runningTotal = 0;                     

				# Keep a running total of the last 10 IBI values
				# Shift data in the rate array
				for i in range(0,9):                
					rate[i] = rate[i+1];                   
					runningTotal += rate[i];               

				# Average and calculate BPM
				rate[9] = IBI;                          
				runningTotal += rate[9];                
				runningTotal /= 10;                     
				BPM = 60000/runningTotal;               
				print('BPM: {}'.format(BPM))

		# Reset pulse flag and update thresh
		if Signal < thresh and Pulse == True :  
			Pulse = False;                       
			amp = P - T;                         
			thresh = amp/2 + T;                  
			P = thresh;                         
			T = thresh;

		# Set default values when no beats found
		if N > 2500 :                           
			thresh = 512;                      
			P = 512;                           
			T = 512;                           
			lastBeatTime = sampleCounter;              
			firstBeat = True;                  
			secondBeat = False;                
			print("no beats found")
			BPM = 0

		uppLim_BPM = 150
		lowLim_BPM = 45

		# Discard unrealistic data and preserve prev BPM
		if (BPM < lowLim_BPM):
			BPM = 40
		elif (BPM > uppLim_BPM):
			BPM = 200
		elif (BPM == 0):
			BPM = pastBPM

		pulseData = {
			"time": sampleCounter,
			"bpm": BPM  
		}
		
		pastBPM = BPM
		time.sleep(0.01)

	print("Pulse Detector finished")

def pulseMSG():

	global start
	print("Pulse MSG started")

	global BPM
	global pastBPM
	global sampleCounter
	global score
	global pastScore
	global u

	while (start):

		Data = {
			"bpm": round(BPM,2),  
			"score": score,
			"speed": round(maxA,2)
		}
		
		MSG_INFO = client.publish("bpm", json.dumps(Data))
		mqtt.error_string(MSG_INFO.rc)
		print("pulseData published:", json.dumps(Data))
		time.sleep(1)

	print("pulse MSG ended")


# Create 4 threads for different tasks
trackScore = threading.Thread(target=scoreDetector)
measurePulse = threading.Thread(target=pulseDetector)
sendData = threading.Thread(target=pulseMSG)
getMaxA = threading.Thread(target=accelerometer) # alternative = shakeDetector code


# Start the thread
measurePulse.start()

# -------------------------------------------------------------------------------------------

def on_message(client, userdata, msg):

	global start
	
	if msg.payload.decode() == "true":
		start = True
		print("start changed to:", start)
		sendData.start()
		trackScore.start()
		getMaxA.start()

	if msg.payload.decode() == "false":
		start = False
		print("start changed to:", start)

	print(f"{msg.topic} + {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):

	print("Subscribed: "+str(mid))

client = mqtt.Client()

# client.tls_set(ca_certs="/home/pi/ca_certificates/ca.crt", 
#                certfile="/home/pi/client_keys/pi.crt",
#                keyfile="/home/pi/client_keys/pi.key")

client.on_subscribe = on_subscribe
client.on_message = on_message

client.username_pw_set("TeamTokyo", "TeamTokyo")
client.connect(host="18.133.234.200")
client.subscribe("StartTransmission")

client.loop_forever()

