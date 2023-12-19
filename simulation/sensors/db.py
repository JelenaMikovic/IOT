from queue import Empty
import RPi.GPIO as GPIO
import time

class DB(object):
    def __init__(self, buzzer_pin = 17):
        self.BUZZER_PIN = buzzer_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)

    def buzz(self, duration, pitch):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.BUZZER_PIN, True)
            time.sleep(delay)
            GPIO.output(self.BUZZER_PIN, False)
            time.sleep(delay)

    def run_db_loop(db, db_queue, pitch, duration, delay, stop_event, publish_event, settings):
        while True:
            try:
                buzz = db_queue.get(timeout=1)
                if buzz:
                    db.buzz(pitch, duration)
            except Empty:
                pass
            if stop_event.is_set():
                GPIO.cleanup()
                break
            time.sleep(delay) 