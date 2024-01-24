import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME
import json

def run_lcd_simulator(delay,text, callback, stop_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("topic/gdht/data")     # data from garage dht
    mqtt_client.on_message = lambda client, userdata, message: on_message_recived(callback, settings, message)
    
    while True:
        if stop_event.is_set():
            break

def on_message_recived(callback, settings, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    callback(data["Temperature"], data["Humidity"])