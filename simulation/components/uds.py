from locks import lock 
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

uds_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()


def publisher_task(event, uds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_uds_batch = uds_batch.copy()
            publish_data_counter = 0
            uds_batch.clear()
        publish.multiple(local_uds_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} uds values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def uds_callback(distance, publish_event, uds_settings, verbose=False):
    global publish_data_counter, publish_data_limit, uds_batch

    if verbose:
        t = time.localtime()
        with lock:       
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Distance: {distance}")
    
    distance_payload = {
        "measurement": "Distance",
        "simulated": uds_settings['simulated'],
        "runs_on": uds_settings["runs_on"],
        "name": uds_settings["name"],
        "value": distance
    }

    with counter_lock:
        uds_batch.append(('topic/uds/distance', json.dumps(distance_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting UDS sumilator")
            from simulators.uds import run_uds_simulator
            uds_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event, publish_event, settings))
            uds_thread.start()
            threads.append(uds_thread)
            with lock:
                print("UDS sumilator started")
        else:
            from sensors.uds import run_uds_loop, UDS
            with lock:
                print("Starting UDS loop")
            uds = UDS(settings['trig'], settings['echo'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event, publish_event, settings))
            uds_thread.start()
            threads.append(uds_thread)
            with lock:
                print("UDS loop started")
