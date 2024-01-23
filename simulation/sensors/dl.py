from queue import Empty
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

class DL(object):
    def __init__(self, light_pin = 18):
        self.LIGHT_PIN = light_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LIGHT_PIN, GPIO.OUT)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("DPIR1")

    def turn_on(self):
        GPIO.output(self.LIGHT_PIN, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.LIGHT_PIN, GPIO.LOW)
    
    def light_triggered(self,callback, publish_event, settings, message):
        self.turn_on()
        callback(True, publish_event, settings)
        time.sleep(10)
        self.turn_off()
        callback(False, publish_event, settings)

    def run_db_loop(dl, dl_queue, delay, callback, stop_event):
        dl.mqtt_client.on_message = lambda client, userdata, message: dl.light_triggered(callback, publish_event, settings, message)
        while True:
            if stop_event.is_set():
                GPIO.cleanup()
                break
            time.sleep(delay) 