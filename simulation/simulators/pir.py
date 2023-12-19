import time
import random

def generate_values():
    detected= True
    while True:
        a = random.randint(1,10)
        if(a>5):
            detected = False
        else:
            detected = True
        yield detected


def run_pir_simulator(delay, no_motion_detected_callback, motion_detected_callback, stop_event, publish_event, settings):
        for value in generate_values():
            if value:
                motion_detected_callback(publish_event, settings)
            else:
                no_motion_detected_callback(publish_event, settings)
            if stop_event.is_set():
                  break
            time.sleep(delay)

