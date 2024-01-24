import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)
mqtt_client.loop_start()

def generate_value(initial_distance = 15):
    distance = initial_distance + random.randint(-10, 10)
    if distance < 0:
        distance = 0
    return distance

def motion_detected(callback, publish_event, settings, message):
    first_distance = generate_value()
    callback(first_distance, publish_event, settings)
    second_distance = generate_value(first_distance)
    callback(second_distance, publish_event, settings)
    if(first_distance < second_distance):
        mqtt_client.publish(settings['name'], "going")
    else:
        mqtt_client.publish(settings['name'], "coming")

def run_uds_simulator(delay, callback, stop_event, publish_event, settings):
    if(settings['name'] == "DUS1"):
        mqtt_client.subscribe("DPIR1")
    if(settings['name'] == "DUS2"):
        mqtt_client.subscribe("DPIR2")
    mqtt_client.on_message = lambda client, userdata, message: motion_detected(callback, publish_event, settings, message)
    while True:
        if stop_event.is_set():
            break