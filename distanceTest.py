import time
import VL53L0X
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect(host="13.42.16.196",port=8883)
client.tls_set(ca_certs="/home/pi/ca_certificates/ca.crt", 
               certfile="/home/pi/client_keys/pi.crt",
               keyfile="/home/pi/client_keys/pi.key")
on_message = client.on_message
client.subscribe("IC.embedded/TeamTokyo/test")
client.loop()

# Enable time in seconds
enable_time = 60
print ("Enable time: %ds" % (enable_time))

score = 0;
print("Initial Score: ", score)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
#VL53L0X_GOOD_ACCURACY_MODE     # Good Accuracy mode
#VL53L0X_BETTER_ACCURACY_MODE   # Better Accuracy mode
#VL53L0X_BEST_ACCURACY_MODE     # Best Accuracy mode
#VL53L0X_LONG_RANGE_MODE        # Longe Range mode
#VL53L0X_HIGH_SPEED_MODE        # High Speed mode

tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)

timing = 0.0950
print ("Timing %d ms" % (timing*1000))

# Calibrate diameter of hoop
avg_distance = tof.calibrate(timing, tof.get_distance())
boundary = avg_distance*0.1

Sensordata1 = {
  "enable time": enable_time,
  "diameter": avg_distance,
  "detection boundary": boundary,
}

json_string1 = json.dumps(Sensordata1)
MSG_INFO = client.publish("test",json_string1)
mqtt.error_string(MSG_INFO.rc)

# Detect if distance decreases
for count in range(1,enable_time*10+1):
    distance = tof.get_distance()
    Sensordata2, score, count = tof.detect(distance, boundary, count, score)
    print("Score : ", score)
    
    json_string2 = json.dumps(Sensordata2)
    MSG_INFO = client.publish("IC.embedded/GROUP_NAME/test",json_string2)
    mqtt.error_string(MSG_INFO.rc)

    time.sleep(timing)

tof.stop_ranging()



def on_message(client, userdata, message) :
 	print("Received message:{} on topic {}".format(message.payload, message.topic))