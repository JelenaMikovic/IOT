from locks import lock 
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ds_batch = ds_batch.copy()
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} ds values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ds_callback(publish_event, ds_settings, verbose=False):
    global publish_data_counter, publish_data_limit, last_time_pressed

    if verbose:
        t = time.localtime()
        with lock:       
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")

    button_payload = {
        "measurement": "Button",
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "name": ds_settings["name"],
        "value": "Button pressed."
    }

    with counter_lock:
        ds_batch.append(('topic/ds/button', json.dumps(button_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ds(settings, threads, stop_event):
        if settings['simulated']:
            with lock:       
                print("Starting DS sumilator")
            from simulators.ds import run_ds_simulator
            ds_thread = threading.Thread(target = run_ds_simulator, args=(2, ds_callback, stop_event, publish_event, settings))
            ds_thread.start()
            threads.append(ds_thread)
            with lock:       
                print("DS sumilator started")
        else:
            from simulation.sensors.ds import run_ds_loop, DS
            with lock:       
                print("Starting DS loop")
            ds = DS(settings['pin'])
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds, 1, ds_callback, stop_event, publish_event, settings))
            ds_thread.start()
            threads.append(ds_thread)
            with lock:       
                print("DS loop started")
