import time
import ads1115

# import json
# from os import path


import paho.mqtt.client as mqtt

filename = 'data.json'
dictObj = []
 
# Check if file exists
if path.isfile(filename) is False:
	raise Exception("File not found")
 
# Read JSON file
with open(filename) as fp:
	dictObj = json.load(fp)
 
# Verify existing dict
print(dictObj)
print(type(dictObj))
 
dictObj.update({"Age": 12,"Role": "Developer"})
 
with open(filename, 'w') as json_file:
	json.dump(dictObj, json_file, 
			indent=4,  
			separators=(',',': '))
 
print('Successfully written to the JSON file')

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("TeamTokyo", "TeamTokyo")
client.connect("13.42.16.196",port=8883)
client.tls_set(ca_certs="ca_certificates/ca.crt", certfile="client_keys/pi.crt", keyfile="client_keys/pi.key")


start = True

if __name__ == '__main__':

  adc = ads1115.ADS1115()

  # initialization 
  GAIN = 2/3  
  thresh = 525  # mid point in the waveform
  P = 512
  T = 512
  sampleCounter = 0
  lastBeatTime = 0
  firstBeat = True
  secondBeat = False
  Pulse = False
  IBI = 600
  rate = [0]*10
  amp = 100

  lastTime = int(time.time()*1000)
  while True:
      # read from the ADC
      Signal = adc.read_adc(0, gain=GAIN)   # Select the A0 channel
      curTime = int(time.time()*1000)

      sampleCounter += curTime - lastTime;  # Keep track of the time in mS
      lastTime = curTime
      N = sampleCounter - lastBeatTime;     # Monitor the time since the last beat to avoid noise

      # Find the peak and trough of the pulse wave
      if Signal < thresh and N > (IBI/5.0)*3.0 :  # Avoid dichrotic noise by waiting 3/5 of last IBI
          if Signal < T :                        # T is the trough
            T = Signal;                         # Keep track of lowest point in pulse wave 

      if Signal > thresh and  Signal > P:           # Thresh condition helps avoid noise
          P = Signal;                             # P is the peak
                                              # keep track of highest point in pulse wave

        # Signal surges up in value every time there is a pulse
      
      if N > 250 :                                   # Avoid high frequency noise
          if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
            Pulse = True;                               # Set the Pulse flag when we think there is a pulse
            IBI = sampleCounter - lastBeatTime;         # Measure time between beats in mS
            lastBeatTime = sampleCounter;               # Keep track of time for next pulse

            if secondBeat :                        # If this is the second beat, if secondBeat == TRUE
              secondBeat = False;                  # Clear secondBeat flag
              for i in range(0,10):             # Seed the running total to get a realisitic BPM at startup
                rate[i] = IBI;                      

            if firstBeat :                        # If it's the first time we found a beat, if firstBeat == TRUE
              firstBeat = False;                   # Clear firstBeat flag
              secondBeat = True;                   # Set the second beat flag
              continue                              # IBI value is unreliable so discard it


            # Keep a running total of the last 10 IBI values
            runningTotal = 0;                  # Clear the runningTotal variable    

            for i in range(0,9):                # Shift data in the rate array
              rate[i] = rate[i+1];                  # and drop the oldest IBI value 
              runningTotal += rate[i];              # Add up the 9 oldest IBI values

            rate[9] = IBI;                          # Add the latest IBI to the rate array
            runningTotal += rate[9];                # Add the latest IBI to runningTotal
            runningTotal /= 10;                     # Average the last 10 IBI values 
            BPM = 60000/runningTotal;               # How many beats can fit into a minute? that's BPM!
            print('BPM: {}'.format(BPM))

      if Signal < thresh and Pulse == True :   # When the values are going down, the beat is over
          Pulse = False;                         # Reset the Pulse flag so we can do it again
          amp = P - T;                           # Get amplitude of the pulse wave
          thresh = amp/2 + T;                    # Set thresh at 50% of the amplitude
          P = thresh;                            # Reset these for next time
          T = thresh;

      if N > 2500 :                          # If 2.5 seconds go by without a beat
          thresh = 512;                          # set thresh default
          P = 512;                               # set P default
          T = 512;                               # set T default
          lastBeatTime = sampleCounter;          # bring the lastBeatTime up to date        
          firstBeat = True;                      # set these to avoid noise
          secondBeat = False;                    # when we get the heartbeat back
          print("no beats found")

      time.sleep(0.005)
      

	adc = ads1x15.ADS1115()
	# initialization 
	GAIN = 2/3  
	curState = 0
	thresh = 525  # mid point in the waveform
	P = 512
	T = 512
	stateChanged = 0
	sampleCounter = 0
	lastBeatTime = 0
	firstBeat = True
	secondBeat = False
	Pulse = False
	IBI = 600
	rate = [0]*10
	amp = 100

	lastTime = int(time.time()*1000)

	while True:
  
		Signal = adc.read_adc(0, gain=GAIN)  
		curTime = int(time.time()*1000)

		sampleCounter += curTime - lastTime;  
		lastTime = curTime
		N = sampleCounter - lastBeatTime;     
  
		if Signal < thresh and N > (IBI/5.0)*3.0 : 
			if Signal < T :                        
				T = Signal;                        

		if Signal > thresh and  Signal > P:          
			P = Signal;                             
											
			if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
				Pulse = True;                               
				IBI = sampleCounter - lastBeatTime;         
				lastBeatTime = sampleCounter;               

				if secondBeat :                        
					secondBeat = False;               
					for i in range(0,10):              
						rate[i] = IBI;                      

				if firstBeat :                        
					firstBeat = False;               
					secondBeat = True;               
					continue                         


				runningTotal = 0;                   

				for i in range(0,9):                
					rate[i] = rate[i+1];                  
					runningTotal += rate[i];              

				rate[9] = IBI;                          
				runningTotal += rate[9];               
				runningTotal /= 10;                     
				BPM = 60000/runningTotal;               
				print('BPM: {}'.format(BPM))
				MSG_INFO = client.publish("test",f"hello from fion {BPM}");
				mqtt.error_string(MSG_INFO.rc);

		if Signal < thresh and Pulse == True :   
			Pulse = False;                        
			amp = P - T;                          
			thresh = amp/2 + T;                 
			P = thresh;                          
			T = thresh;

		if N > 2500 :                         
			thresh = 512;                      
			P = 512;                           
			T = 512;                           
			lastBeatTime = sampleCounter;             
			firstBeat = True;                   
			secondBeat = False;                 
			print("no beats found")
			MSG_INFO = client.publish("test",f"hello from fion: no beats found");
			mqtt.error_string(MSG_INFO.rc);

		time.sleep(0.005)

