import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)
mqtt_client.loop_start()

def generate_values():
    open = True
    while True:
        a = random.randint(1,10)
        if(a>2):
            open = False
        else:
            open = True
        yield open

def run_ds_simulator(delay, callback, stop_event, publish_event, settings):
    for value in generate_values():
        time.sleep(delay)
        if value:
            callback(publish_event, settings)
            a = random.randint(1,8)
            if a >= 5:
                mqtt_client.publish("topic/alarm", "on")
                print("ALARM PRESS DETECTED")
                time.sleep(a)
                mqtt_client.publish("topic/alarm", "off")
                print("NO ALARM PRESS DETECTED")
        if stop_event.is_set():
            break