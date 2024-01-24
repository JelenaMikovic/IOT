import threading
from locks import lock
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dl_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} dl values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(active, publish_event, dl_settings, verbose=False):
    global publish_data_counter, publish_data_limit
    
    if verbose:
        t = time.localtime()
        with lock:
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if active:  
                print(f"Doorlight is on")
            else:
                print(f"Doorlight is off")

    light_payload = {
        "measurement": "Light",
        "simulated": dl_settings['simulated'],
        "runs_on": dl_settings["runs_on"],
        "name": dl_settings["name"],
        "value": active
    }

    with counter_lock:
        dl_batch.append(('topic/dl/light', json.dumps(light_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dl(settings, threads, stop_event, queue):
        if settings['simulated']:
            with lock:
                print("Starting DL sumilator")
            from simulators.dl import run_dl_simulator
            dl_thread = threading.Thread(target = run_dl_simulator, args=(queue, 2, dl_callback, stop_event, publish_event, settings))
            dl_thread.start()
            threads.append(dl_thread)
            with lock:
                print("DL sumilator started")
        else:
            from simulation.sensors.dl import run_dl_loop, DL
            with lock:
                print("Starting DL loop")
            dl = DL(settings['pin'])
            dl_thread = threading.Thread(target=run_dl_loop, args=(dl, queue, 2, dl_callback, stop_event, publish_event, settings))
            dl_thread.start()
            threads.append(dl_thread)
            with lock:
                print("DL loop started")

