import RPi.GPIO as GPIO
from locks import lock
import time

from simulation.components.pir import motion_detected_callback
from simulation.components.pir import no_motion_detected_callback


class PIR(object):
    def __init__(self, pin=4):
        self.PIR_PIN = pin

    def motion_detect(self, publish_event, settings):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIR_PIN,GPIO.IN)
        GPIO.add_event_detect(self.PIR_PIN,GPIO.RISING,callback=motion_detected_callback(publish_event,settings))
        GPIO.add_event_detect(self.PIR_PIN,GPIO.FALLING,callback=no_motion_detected_callback(publish_event,settings))


    def run_pir_loop(pir, delay, stop_event, publish_event, settings):
        while True:
            pir.motion_detect(publish_event,settings)
            if stop_event.is_set():
                    break
            time.sleep(delay)