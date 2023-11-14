from simulation.simulators.pir import run_pir_simulator
import threading
import time

def pir_callback(motion_detected, code):
    if motion_detected:
           t = time.localtime()
           print("="*20)
           print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
           print(f"Code: {code}")
           print(f"Motion detected\n")

def run_pir(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting pir sumilator")
            pir_thread = threading.Thread(target = run_pir_simulator, args=(2, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print("pir simulator started")
        else:
            from simulation.sensors.pir import run_pir_loop, PIR
            print("Starting pir loop")
            pir = PIR(settings['pin'])
            pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print("pir loop started")
