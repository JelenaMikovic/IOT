import RPi.GPIO as GPIO
import time

class Button(object):
    def __init__(self, port):
        self.PORT_BUTTON = port

    def button_pressed(self,event):
        print("BUTTON PRESS DETECTED")

    def detect_button_press(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PORT_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.PORT_BUTTON, GPIO.RISING, callback =
        self.button_pressed, bouncetime = 100)

    def run_db_loop(ds, delay, callback, stop_event):
		while True:
			check = ds.readDHT11()
			if stop_event.is_set():
					break
			time.sleep(delay)  # Delay between readings
