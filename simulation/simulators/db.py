from queue import Empty
from locks import lock
import time
import random

def run_db_simulator(queue, pitch, duration, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = queue.get(timeout=1)
            if action:
                callback(True, publish_event, settings)
                period = 1.0 / pitch
                delay = period / 2
                cycles = int(duration * pitch) 
                
                with lock:
                    for _ in range(cycles):
                        start = time.time()
                        while True:
                            if time.time() - start > delay:
                                break
                            if pitch > 1000:
                                print("!", end="")
                            elif pitch > 500:
                                print("=", end="")
                            else:
                                print("_", end="")
                        print("\n")
                        time.sleep(delay)
                        if stop_event.is_set():
                            break
                callback(False, publish_event, settings)
        except Empty:
            pass

