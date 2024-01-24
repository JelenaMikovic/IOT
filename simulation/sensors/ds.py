import RPi.GPIO as GPIO
from locks import lock
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT

class DS(object):
    def __init__(self, port):
        self.PORT_BUTTON = port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.button_pressed_time = 0
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.subscribe("topic/system")
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.loop_start()
        self.system = False

    def on_message(self, callback, publish_event, settings, message):
            action = message.payload.decode("utf-8")
            if action == "active":
                this.system = True
            elif action == "deactive":
                this.system = False

    def button_pressed(self, event):
        with lock:
            if this.system:
                print("BUTTON PRESS DETECTED")
                self.button_pressed_time = time.time()  

    def button_released(self, event):
        with lock:
            if this.system:
                print("BUTTON RELEASED")
                if time.time() - self.button_pressed_time >= 5:
                    mqtt_client.publish("topic/alarm", "on")
                else:
                    mqtt_client.publish("topic/alarm", "off")

    def detect_button_press(self):
        GPIO.add_event_detect(self.PORT_BUTTON, GPIO.RISING, callback=self.button_pressed, bouncetime=100)
        GPIO.add_event_detect(self.PORT_BUTTON, GPIO.FALLING, callback=self.button_released, bouncetime=100)

    def run_ds_loop(self, db, delay, stop_event, publish_event, settings):
        while True:
            if stop_event.is_set():
                break

            time.sleep(delay)