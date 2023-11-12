import time
import random

def generate_values(initial_distance = 15):
      while True:
            distance = initial_distance + random.randint(-10, 10)
            if distance > 10:
                distance = None
            yield distance

      

def run_uds_simulator(delay, callback, stop_event):
        for h, t in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(h, t)
            if stop_event.is_set():
                  break
              