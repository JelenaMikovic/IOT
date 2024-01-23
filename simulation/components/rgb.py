from ctypes import sizeof
from locks import lock
import threading
import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} pir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch))
publisher_thread.daemon = True
publisher_thread.start()

def callback(publish_event, rgb_settings, mode, verbose=False):
    global publish_data_counter, publish_data_limit, rgb_batch
    
    no_movement_payload = {
        "measurement": "Light",
        "simulated": rgb_settings['simulated'],
        "runs_on": rgb_settings["runs_on"],
        "name": rgb_settings["name"],
        "value": mode
    }     

    with counter_lock:
        rgb_batch.append(("topic/rgb/light", json.dumps(no_movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_rgb(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting RGB sumilator")
            from simulators.rgb import run_rgb_simulator
            rgb_thread = threading.Thread(target = run_rgb_simulator, args=(5, callback, stop_event, publish_event, settings))
            rgb_thread.start()
            threads.append(rgb_thread)
            with lock:
                print("RGB simulator started")
        else:
            from simulation.sensors.rgb import run_rgb_loop, RGB
            with lock:
                print("Starting RGB loop")
            rgb = RGB(settings, callback)
            rgb_thread = threading.Thread(target=run_rgb_loop, args=(rgb))
            rgb_thread.start()
            threads.append(rgb_thread)
            with lock:
                print("RGB loop started")
