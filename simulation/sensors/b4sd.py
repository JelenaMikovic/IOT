import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class B4sd(object):
    num = {
        ' ':(0,0,0,0,0,0,0),
        '0':(1,1,1,1,1,1,0),
        '1':(0,1,1,0,0,0,0),
        '2':(1,1,0,1,1,0,1),
        '3':(1,1,1,1,0,0,1),
        '4':(0,1,1,0,0,1,1),
        '5':(1,0,1,1,0,1,1),
        '6':(1,0,1,1,1,1,1),
        '7':(1,1,1,0,0,0,0),
        '8':(1,1,1,1,1,1,1),
        '9':(1,1,1,1,0,1,1)
        }

    def __init__(self, settings):
        self.segments = settings['segments']
        self.digits = settings['digits']
        GPIO.setmode(GPIO.BCM)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe("topic/db/clock")
        self.mqtt_client.loop_start()
        self.blinking = False

        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
    
    def on_message(self, callback, publish_event, settings, message):
        action = message.payload.decode("utf-8")
        if action == "clockOn":
            self.blinking = True
        elif action == "clockOff":
            self.blinking = False
            
    def run_b4sd_loop(self, settings, stop_event, callback, publish_event):
        try:
            while True:
                if self.stop_event.is_set():
                    self._stop()
                    break

            if self.blinking:
                n = time.ctime()[11:13] + time.ctime()[14:16]
                s = str(n).rjust(4)
                for _ in range(2): 
                    for digit in range(4):
                        for loop in range(0, 7):
                            if _ == 0:
                                GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                            else:
                                GPIO.output(self.segments[loop], 0)

                        if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                            GPIO.output(25, 1)
                        else:
                            GPIO.output(25, 0)

                        GPIO.output(self.digits[digit], 0)
                        time.sleep(0.001)
                        GPIO.output(self.digits[digit], 1)
                    time.sleep(0.5)

            else:
                n = time.ctime()[11:13] + time.ctime()[14:16]
                s = str(n).rjust(4)
                for digit in range(4):
                    for loop in range(0, 7):
                        GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                    if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                        GPIO.output(25, 1)
                    else:
                        GPIO.output(25, 0)
                    GPIO.output(self.digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(self.digits[digit], 1)
                self.callback(self.settings, s, self.publish_event)

        finally:
            GPIO.cleanup()

