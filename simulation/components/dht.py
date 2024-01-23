from locks import lock
import threading
import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, 1883, 60)

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dht values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht_callback(humidity, temperature, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with lock: 
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Humidity: {humidity}%")
            print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append(('topic/dht/temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('topic/dht/humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1
    
    if dht_settings['name'] == "GDHT":
        mqtt_client.publish('topic/gdht/humidity', humidity)
        mqtt_client.publish('topic/gdht/temperature', temperature)

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            with lock: 
                print("Starting {} sumilator", settings["name"])
            from simulators.dht import run_dht_simulator
            dht_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event, publish_event, settings))
            dht_thread.start()
            threads.append(dht_thread)
            with lock: 
                print("{} sumilator started", settings["name"])
        else:
            from simulation.sensors.dht import run_dht_loop, DHT
            with lock: 
                print("Starting {} loop", settings["name"])
            dht = DHT(settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, publish_event, settings))
            dht_thread.start()
            threads.append(dht_thread)
            with lock: 
                print("{} loop started", settings["name"])
