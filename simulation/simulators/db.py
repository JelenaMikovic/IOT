from queue import Empty
from locks import lock
import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)
mqtt_client.loop_start()
mqtt_client.subscribe("topic/alarm")
mqtt_client.subscribe("topic/system")
buzzing = False
system = False

def on_message(callback, publish_event, settings, message):
    global buzzing, system
    action = message.payload.decode("utf-8")
    if system:
        if action == "on":
            buzzing = True
            callback(True, publish_event, settings)
        elif action == "off":
            buzzing = False
            callback(False, publish_event, settings)
    if action == "active":
        system = True
    elif action == "deactive":
        system = False

def run_db_simulator(queue, pitch, duration, callback, stop_event, publish_event, settings):
    mqtt_client.on_message = lambda client, userdata, message: on_message(callback, publish_event, settings, message)
    while not stop_event.is_set():
        try:
            global buzzing
            if buzzing:
                period = 1.0 / pitch
                delay = period / 2
                cycles = int(duration * pitch) 
                with lock:
                    for _ in range(cycles):
                        start = time.time()
                        while True:
                            if time.time() - start > delay:
                                break
                            if pitch > 1000:
                                print("!", end="")
                            elif pitch > 500:
                                print("=", end="")
                            else:
                                print("_", end="")
                        print("\n")
                        time.sleep(delay)
                        if stop_event.is_set():
                            break
        except Empty:
            pass

