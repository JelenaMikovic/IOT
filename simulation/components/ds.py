from simulation.simulators.ds import run_ds_simulator
from locks import lock 
import threading
import time

def ds_callback():
    t = time.localtime()
    with lock:       
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")

def run_ds(settings, threads, stop_event):
        if settings['simulated']:
            with lock:       
                print("Starting DS sumilator")
            ds_thread = threading.Thread(target = run_ds_simulator, args=(2, ds_callback, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            with lock:       
                print("DS sumilator started")
        else:
            from simulation.sensors.ds import run_ds_loop, DS
            with lock:       
                print("Starting DS loop")
            ds = DS(settings['pin'])
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds, 2, ds_callback, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            with lock:       
                print("DS loop started")
