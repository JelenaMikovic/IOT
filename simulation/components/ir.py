import threading
from locks import lock
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ir_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ir_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        publish.multiple(local_ir_batch, hostname=HOSTNAME, port=PORT)
        #print(f'published {publish_data_limit} ir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ir_callback(publish_event, ir_settings, hue, verbose=False):
    global publish_data_counter, publish_data_limit
    
    light_payload = {
        "measurement": "Hue",
        "simulated": ir_settings['simulated'],
        "runs_on": ir_settings["runs_on"],
        "name": ir_settings["name"],
        "value": hue
    }

    with counter_lock:
        ir_batch.append(('topic/ir/hue', json.dumps(light_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ir(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting IR sumilator")
            from simulators.ir import run_ir_simulator
            ir_thread = threading.Thread(target = run_ir_simulator, args=(ir_callback, stop_event, settings, publish_event))
            ir_thread.start()
            threads.append(ir_thread)
            with lock:
                print("IR sumilator started")
        else:
            from simulation.sensors.ir import run_ir_loop, IR
            with lock:
                print("Starting IR loop")
            ir = IR(settings, stop_event, ir_receiver_callback, publish_event)
            ir_thread = threading.Thread(target=ir.run(), args=())
            ir_thread.start()
            threads.append(ir_thread)
            with lock:
                print("IR loop started")

