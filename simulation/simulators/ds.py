import time
import random

def generate_values():
    open = True
    while True:
        a = random.randint(1,10)
        if(a>5):
            open = False
        else:
            open = True
        yield open

def run_ds_simulator(delay, callback, stop_event):
    for value in generate_values():
        time.sleep(delay)
        if value:
            callback()
        if stop_event.is_set():
                break
