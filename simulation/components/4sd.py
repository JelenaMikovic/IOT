from locks import lock
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

b4sd_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, b4sd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_b4sd_batch = b4sd_batch.copy()
            publish_data_counter = 0
            b4sd_batch.clear()
        publish.multiple(local_b4sd_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} b4sd values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, b4sd_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def b4sd_callback(settings, segment, publish_event):
    b4sd_payload ={
        "measurement": "Segment",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": segment,
    } 

    with counter_lock:
        b4sd_batch.append(('topic/b4sd/segment', json.dumps(b4sd_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    
def run_b4sd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting B4SD simulator")
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(settings, stop_event, b4sd_callback, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("B4SD simulator started")
    else:
        from sensors.b4sd import B4sd
        print("Starting B4SD loop")
        b4sd = B4sd(settings, stop_event, b4sd_callback)
        b4sd_thread = threading.Thread(target=b4sd.run(), args=(settings, stop_event, b4sd_callback, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("B4SD loop started")