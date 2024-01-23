from ctypes import sizeof
from locks import lock
import threading
import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)

def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} pir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch))
publisher_thread.daemon = True
publisher_thread.start()

def motion_detected_callback(publish_event, pir_settings, verbose=False):
    global publish_data_counter, publish_data_limit, pir_batch
    t = time.localtime()
    if verbose:
        with lock:
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print("You moved!")
    
    movement_payload = {
        "measurement": "Movement",
        "simulated": pir_settings["simulated"],
        "runs_on": pir_settings["runs_on"],
        "name": pir_settings["name"],
        "value": True
    }   
    
    with counter_lock:
        pir_batch.append(("topic/pir/movement", json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    
    mqtt_client.publish(pir_settings['name'], "motion")

def no_motion_detected_callback(publish_event, pir_settings, verbose=False):
    global publish_data_counter, publish_data_limit, pir_batch
    t = time.localtime()
    if verbose:    
        with lock:
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print("You stopped moving!")
    
    no_movement_payload = {
        "measurement": "Movement",
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "name": pir_settings["name"],
        "value": False
    }     

    with counter_lock:
        pir_batch.append(("topic/pir/movement", json.dumps(no_movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_pir(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting PIR sumilator")
            from simulators.pir import run_pir_simulator
            pir_thread = threading.Thread(target = run_pir_simulator, args=(5, no_motion_detected_callback, motion_detected_callback, stop_event, publish_event, settings))
            pir_thread.start()
            threads.append(pir_thread)
            with lock:
                print("PIR simulator started")
        else:
            from simulation.sensors.pir import run_pir_loop, PIR
            with lock:
                print("Starting PIR loop")
            pir = PIR(settings['pin'])
            pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, stop_event, publish_event, settings))
            pir_thread.start()
            threads.append(pir_thread)
            with lock:
                print("PIR loop started")
