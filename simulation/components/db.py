from simulation.simulators.db import run_db_simulator
from locks import lock
import threading
import time

def db_callback(active):
    t = time.localtime()
    with lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        if active:  
            print(f"Doorbell is buzzing")
        else:
            print(f"Doorbell stopped buzzing")


def run_db(settings, threads, stop_event, queue):
        delay, pitch, duration = 1, 1000, 0.1
        if settings['simulated']:
            with lock:
                print("Starting DB sumilator")
            db_thread = threading.Thread(target = run_db_simulator, args=(queue, pitch, duration, db_callback, stop_event))
            db_thread.start()
            threads.append(db_thread)
            with lock:
                print("DB sumilator started")
        else:
            from simulation.sensors.db import run_db_loop, DB
            with lock:
                print("Starting DB loop")
            db = DB(settings['pin'])
            db_thread = threading.Thread(target=run_db_loop, args=(db, queue, pitch, duration, delay, stop_event))
            db_thread.start()
            threads.append(db_thread)
            with lock:
                print("DB loop started")

