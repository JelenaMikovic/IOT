from locks import lock
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

db_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, db_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_db_batch = db_batch.copy()
            publish_data_counter = 0
            db_batch.clear()
        publish.multiple(local_db_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, db_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def db_callback(active, publish_event, db_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with lock:
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if active:  
                print(f"Doorbell is buzzing")
            else:
                print(f"Doorbell stopped buzzing")

    door_payload = {
        "measurement": "Dorbell",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
        "value": active
    }

    with counter_lock:
        db_batch.append(('topic/db/buzz', json.dumps(door_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_db(settings, threads, stop_event, queue):
        delay, pitch, duration = 1, 1000, 0.1
        if settings['simulated']:
            with lock:
                print("Starting DB sumilator")
            from simulators.db import run_db_simulator
            db_thread = threading.Thread(target = run_db_simulator, args=(queue, pitch, duration, db_callback, stop_event, publish_event, settings))
            db_thread.start()
            threads.append(db_thread)
            with lock:
                print("DB sumilator started")
        else:
            from simulation.sensors.db import run_db_loop, DB
            with lock:
                print("Starting DB loop")
            db = DB(settings['pin'])
            db_thread = threading.Thread(target=run_db_loop, args=(db, queue, pitch, duration, delay, stop_event, publish_event, settings))
            db_thread.start()
            threads.append(db_thread)
            with lock:
                print("DB loop started")

