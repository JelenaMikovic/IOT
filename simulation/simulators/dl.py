from queue import Empty
import time

def run_dl_simulator(queue, delay, callback, stop_event):
    while not stop_event.is_set():
        try:
            action = queue.get(timeout=1)
            if action:
                callback(True)
            else:
                callback(False)
        except Empty:
            pass
        time.sleep(delay)

