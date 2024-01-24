from tabnanny import verbose
from locks import lock
import threading
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT
import json

ms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
system = "6253"
pin = "4507"
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)

def publisher_task(event, ms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ms_batch = ms_batch.copy()
            publish_data_counter = 0
            ms_batch.clear()
        publish.multiple(local_ms_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ms values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ms_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ms_callback(key_pressed, publish_event, ms_settings, verbose=False):
    global publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        with lock:
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Key pressed: {key_pressed}")
    key_payload = {
        "measurement": "KeyPressed",
        "simulated": ms_settings['simulated'],
        "runs_on": ms_settings["runs_on"],
        "name": ms_settings["name"],
        "value": key_pressed
    }

    if(system != key_pressed):
        time.sleep(10)
        mqtt_client.publish('topic/alarm', "on")
    elif(pin != key_pressed):
        mqtt_client.publish('topic/alarm', "off")
        mqtt_client.publish('topic/system', "deactive")
    else:
        mqtt_client.publish('topic/system', "active")

    with counter_lock:
        ms_batch.append(("topic/ms/keypressed", json.dumps(key_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ms(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting MS sumilator")
            from simulators.ms import run_ms_simulator
            ms_thread = threading.Thread(target = run_ms_simulator, args=(2, ms_callback, stop_event, publish_event, settings))
            ms_thread.start()
            threads.append(ms_thread)
            with lock:
                print("MS sumilator started")
        else:
            from simulation.sensors.ms import run_ms_loop, MS
            with lock:
                print("Starting MS loop")
            ms = MS(R1=settings["R1"], R2=settings["R2"],  R3=settings["R3"],  R4=settings["R4"], C1=settings["C1"], C2=settings["C2"], C3=settings["C3"], C4=settings["C4"])
            ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event, publish_event, settings))
            ms_thread.start()
            threads.append(ms_thread)
            with lock:
                print("MS loop started")

