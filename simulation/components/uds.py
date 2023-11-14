from simulators.uds import run_uds_simulator
from locks import lock 
import threading
import time

def uds_callback(distance):
    t = time.localtime()
    with lock:       
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Distance: {distance}")

def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting UDS sumilator")
            uds_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            with lock:
                print("UDS sumilator started")
        else:
            from sensors.uds import run_uds_loop, UDS
            with lock:
                print("Starting UDS loop")
            uds = UDS(settings['trig'], settings['echo'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            with lock:
                print("UDS loop started")
