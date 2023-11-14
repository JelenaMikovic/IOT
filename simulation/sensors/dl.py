from queue import Empty
import RPi.GPIO as GPIO
import time

class DL(object):
    def __init__(self, light_pin = 18):
        self.LIGHT_PIN = light_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LIGHT_PIN, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.LIGHT_PIN, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.LIGHT_PIN, GPIO.LOW)

    def run_db_loop(dl, dl_queue, delay, stop_event):
        while True:
            try:
                switch = dl_queue.get(timeout=1)
                if switch:
                    dl.turn_on()
                else:
                    dl.turn_off()
            except Empty:
                pass
            if stop_event.is_set():
                GPIO.cleanup()
                break
            time.sleep(delay) 