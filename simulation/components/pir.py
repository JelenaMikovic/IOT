from locks import lock
import threading
import time

def motion_detected_callback(channel=None):
    t = time.localtime()
    with lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("You moved!")

def no_motion_detected_callback(channel=None):
    t = time.localtime()
    with lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("You stopped moving!")

def run_pir(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting PIR sumilator")
            from simulators.pir import run_pir_simulator
            pir_thread = threading.Thread(target = run_pir_simulator, args=(2, no_motion_detected_callback, motion_detected_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            with lock:
                print("PIR simulator started")
        else:
            from simulation.sensors.pir import run_pir_loop, PIR
            with lock:
                print("Starting PIR loop")
            pir = PIR(settings['pin'])
            pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            with lock:
                print("PIR loop started")
