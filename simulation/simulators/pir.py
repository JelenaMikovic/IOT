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



def run_pir_simulator(delay, callback, stop_event):
        for h, t in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(h, t)
            if stop_event.is_set():
                  break
