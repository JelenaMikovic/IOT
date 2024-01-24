import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def generate_values():
    while True:
        rotation_x = random.uniform(-10.0, 10.0) 
        rotation_y = random.uniform(-10.0, 10.0)  
        rotation_z = random.uniform(-10.0, 10.0) 
        
        acceleration_x = random.uniform(-50, 50)
        acceleration_y = random.uniform(-50, 50)
        acceleration_z = random.uniform(-50, 50)

        yield {
            "rotation_x": rotation_x / 131.0,
            "rotation_y": rotation_y / 131.0,
            "rotation_z": rotation_z / 131.0,
            "acceleration_x" : acceleration_x / 16384.0,
            "acceleration_y" : acceleration_y / 16384.0,
            "acceleration_z" : acceleration_z / 16384.0
        }


def run_gyro_simulator(delay,callback, stop_event, publish_event, settings):
    threshold = 0.45  # Set your threshold for significant gyroscope movement
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    for gyro_data in generate_values():
        # TODO dodaj proveru za alarm
        time.sleep(delay)  # Delay between readings (adjust as needed)
        callback(gyro_data, publish_event, settings, False)
        if stop_event.is_set():
            break