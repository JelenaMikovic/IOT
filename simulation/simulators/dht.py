import time
import random
import json
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature

      

def run_dht_simulator(delay, callback, stop_event, publish_event, settings):
      mqtt_client = mqtt.Client()
      mqtt_client.connect(HOSTNAME, 1883, 60)
      for h, t in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(h, t, publish_event, settings)
            if(settings["name"] == "GDHT"):
                  data = {"Temperature": t, "Humidity": h}
                  json_data = json.dumps(data)
                  mqtt_client.publish("gdht/data", json_data)
            if stop_event.is_set():
                  break
              