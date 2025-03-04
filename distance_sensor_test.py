#!/usr/bin/python


# Import required Python libraries
import time
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client


#Global variable for distance

ADAFRUIT_USERNAME  = ""
ADAFRUIT_APIKEY = ""

#MQTT Functions
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(ADAFRUIT_USERNAME, ADAFRUIT_APIKEY)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,distance):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"{distance}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 1:
            break
    


#Setup MQTT Broker
broker = "io.adafruit.com"
port = 1883
topic = "schied13/feeds/water-level"
client_id = "rasp"
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24







#Subscribe to client
client = connect_mqtt()
def setup():
    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
    
    
    publish(client,0)
    
    
    
def loop():    
    while True:
        print("Ultrasonic Measurement")

        # Allow module to settle
        time.sleep(5)

        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()

        while GPIO.input(GPIO_ECHO)==0:
          start = time.time()
          

        while GPIO.input(GPIO_ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distancet = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = distancet / 2
        
        publish(client,distance)
        print("Distance :", distance)

        #print("Elaspsed time :", elapsed)

        #print("Total distance :", distancet)

setup()
loop()
# Reset GPIO settings
GPIO.cleanup()
