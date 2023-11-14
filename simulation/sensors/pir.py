import RPi.GPIO as GPIO
import time

class PIR(object):
    def __init__(self, pin=4):
        self.PIR_PIN = pin

    def motion_detected_callback(channel=None):
        print("You moved!")

    def no_motion_callback(channel=None):
        print("You stopped moving!")

    def motion_detect(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIR_PIN,GPIO.IN)
        GPIO.add_event_detect(self.PIR_PIN,GPIO.RISING,callback=self.motion_detected_callback)
        GPIO.add_event_detect(self.PIR_PIN,GPIO.FALLING,callback=self.no_motion_callback)


    def run_pir_loop(pir, delay, callback, stop_event):
		while True:
			check = pir.motion_detect()
			if stop_event.is_set():
					break
			time.sleep(delay)  # Delay between readings
