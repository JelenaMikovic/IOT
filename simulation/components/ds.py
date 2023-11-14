from simulation.simulators.ds import run_ds_simulator
import threading
import time

def ds_callback():
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")

def run_ds(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting ds sumilator")
            ds_thread = threading.Thread(target = run_ds_simulator, args=(2, ds_callback, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds sumilator started")
        else:
            from simulation.sensors.ds import run_ds_loop, DS
            print("Starting ds loop")
            ds = DS(settings['pin'])
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds, 2, ds_callback, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds loop started")
