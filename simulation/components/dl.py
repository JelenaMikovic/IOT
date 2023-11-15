import threading
from locks import lock
import time

def dl_callback(active):
    t = time.localtime()
    with lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        if active:  
            print(f"Doorlight is on")
        else:
            print(f"Doorlight is off")


def run_dl(settings, threads, stop_event, queue):
        if settings['simulated']:
            with lock:
                print("Starting DL sumilator")
            from simulators.dl import run_dl_simulator
            dl_thread = threading.Thread(target = run_dl_simulator, args=(queue, 2, dl_callback, stop_event))
            dl_thread.start()
            threads.append(dl_thread)
            with lock:
                print("DL sumilator started")
        else:
            from simulation.sensors.dl import run_dl_loop, DL
            with lock:
                print("Starting DL loop")
            dl = DL(settings['pin'])
            dl_thread = threading.Thread(target=run_dl_loop, args=(dl, queue, 2, dl_callback, stop_event))
            dl_thread.start()
            threads.append(dl_thread)
            with lock:
                print("DL loop started")

