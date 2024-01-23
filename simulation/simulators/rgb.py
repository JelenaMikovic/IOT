import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def set_light(message, settings, callback, publish_event):
    mode = message.payload.decode("utf-8")
    callback(publish_event ,settings, mode)

def run_rgb_simulator(delay, callback, stop_event, publish_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("topic/rgb")
    mqtt_client.on_message = lambda client, userdata, message: set_light(message, settings, callback, publish_event)