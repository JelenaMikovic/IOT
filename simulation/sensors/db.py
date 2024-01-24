from queue import Empty
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT


class DB(object):
    def __init__(self, buzzer_pin=17):
        self.BUZZER_PIN = buzzer_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe("topic/alarm")
        self.mqtt_client.subscribe("topic/system")
        self.mqtt_client.loop_start()
        self.buzzing = False
        self.system = False

    def on_message(self, callback, publish_event, settings, message):
        action = message.payload.decode("utf-8")
        if this.system:
            if action == "on":
                self.start_buzz()
                callback(True, publish_event, settings)
            elif action == "off":
                self.stop_buzz()
                callback(False, publish_event, settings)
        if action == "active":
            this.system = True
        elif action == "deactive":
            this.system = False

    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.BUZZER_PIN, True)
            time.sleep(delay)
            GPIO.output(self.BUZZER_PIN, False)
            time.sleep(delay)

    def start_buzz(self):
        if not self.buzzing:
            self.buzzing = True
            while self.buzzing:
                self.buzz(440, 1)

    def stop_buzz(self):
        self.buzzing = False

    def cleanup(self):
        GPIO.cleanup()
    

def run_db_loop(db, stop_event):
    db.mqtt_client.on_message = lambda client, userdata, message: db.on_message(callback, publish_event, settings, message)
    db.buzz(pitch, duration)
    while True:
        if stop_event.is_set():
            db.stop_buzz()
            db.cleanup()
            break