import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class RGB(object):
    def __init__(self, settings, callback):
        self.callback = callback
        self.RED_PIN= settings['red_pin']
        self.GREEN_PIN = settings['green_pin']
        self.BLUE_PIN = settings['blue_pin']
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("topic/rgb")
        
    def turnOff(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
    
    def white(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def red(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def green(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def blue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def yellow(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def purple(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def lightBlue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
    
    def run_rgb_loop(self):
        self.mqtt_client.on_message = lambda client, userdata, message: self.set_light(message)
              
    def set_light(self, message):
        mode = message.payload.decode("utf-8")

        if mode == "off":
            self.turnOff()
        elif mode == "red":
            self.red()
        elif mode == "blue":
            self.blue()
        elif mode == "green":
            self.green()
        elif mode == "white":
            self.white()
        elif mode == "yellow":
            self.yellow()
        elif mode == "purple":
            self.purple()
        elif mode == "light_blue":
            self.lightBlue()

        self.callback(self.settings, mode)