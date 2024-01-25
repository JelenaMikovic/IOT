import time 
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)
mqtt_client.loop_start()
mqtt_client.subscribe("topic/db/clock")
blinking = False

def on_message(callback, publish_event, settings, message):
    global blinking
    action = message.payload.decode("utf-8")
    if action == "clockOn":
        blinking = True
    elif action == "clockOff":
        blinking = False

def run_b4sd_simulator(settings, stop_event, callback, publish_event):
    mqtt_client.on_message = lambda client, userdata, message: on_message(callback, publish_event, settings, message)
    while True:
        if stop_event.is_set():
            break

        global blinking
        if blinking:
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            for _ in range(2):  
                callback(settings, s, publish_event)
                time.sleep(0.5)  
                callback(settings, "", publish_event) 
                time.sleep(0.5) 
        else:
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            callback(settings, s, publish_event)
            time.sleep(5)