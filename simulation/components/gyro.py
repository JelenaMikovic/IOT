from simulators.gyro import run_gyro_simulator
import threading
import time
from locks import print_lock
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json


gyro_batch = []
publish_data_counter = 0
publish_data_limit = 6
counter_lock = threading.Lock()

def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gyro_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        publish.multiple(local_gyro_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} gyro values')
        event.clear()
    

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def gyro_callback(gyro_data, publish_event, settings, verbose=True):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    formatted_time = time.strftime('%d.%m.%Y. %H:%M:%S', t)
    if verbose:     
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Rotation x: {gyro_data['rotation_x']}")
            print(f"Rotation y: {gyro_data['rotation_y']}")
            print(f"Rotation z: {gyro_data['rotation_z']}")
            print(f"Acceleration x: {gyro_data['acceleration_x']}")
            print(f"Acceleration y: {gyro_data['acceleration_y']}")
            print(f"Acceleration z: {gyro_data['acceleration_z']}")
            print("="*10)

    print(gyro_data)
    rotation_values = []
    acceleration_values = []
    

    
    rotation_payload = {
        "measurement": "Rotation",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "rotation_x": gyro_data["rotation_x"],
        "rotation_y": gyro_data["rotation_y"],
        "rotation_z": gyro_data["rotation_z"]
    }
    
    acceleration_payload = {
        "measurement": "Acceleration",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "acceleration_x": gyro_data['acceleration_x'],
        "acceleration_y": gyro_data["acceleration_y"],
        "acceleration_z": gyro_data["acceleration_z"],
    }

    with counter_lock:
        gyro_batch.append(('topic/gyro/rotation'), json.dumps(rotation_payload), 0, True)
        gyro_batch.append(('topic/gryo/acceleration'),json.dumps(acceleration_payload), 0, True)
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        gyro_thread = threading.Thread(target=run_gyro_simulator, args=(2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.gyro.gyro import run_gyro_loop, MPU6050
        print("Starting {} loop".format(settings["name"]))
        mpu = MPU6050.MPU6050()
        gyro_thread = threading.Thread(target=run_gyro_loop, args=(mpu, 2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        print("{} loop started".format(settings["name"]))
