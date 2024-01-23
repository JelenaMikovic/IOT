from queue import Empty
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

def run_dl_simulator(queue, delay, callback, stop_event, publish_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("DPIR1")
    mqtt_client.on_message = lambda client, userdata, message: dl_triggered(callback, publish_event, settings, message)

    while not stop_event.is_set():
        pass

def dl_triggered(callback, publish_event, settings, message):
    callback(True, publish_event, settings)
    time.sleep(10)
    callback(False, publish_event, settings)
