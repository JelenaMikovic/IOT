from queue import Empty
import time

def run_dl_simulator(queue, delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = queue.get(timeout=1)
            if action:
                callback(True, publish_event, settings)
            else:
                callback(False, publish_event, settings)
        except Empty:
            pass
        time.sleep(delay)

