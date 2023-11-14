from simulation.simulators.ms import run_ms_simulator
import threading
import time

def ms_callback(keypressed):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Key pressed: {keypressed}")

def run_ms(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting ms sumilator")
            ms_thread = threading.Thread(target = run_ms_simulator, args=(2, ms_callback, stop_event))
            ms_thread.start()
            threads.append(ms_thread)
            print("ms sumilator started")
        else:
            from simulation.sensors.ms import run_ms_loop, MS
            print("Starting ms loop")
            ms = MS(settings['pin'])
            ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event))
            ms_thread.start()
            threads.append(ms_thread)
            print("ms loop started")

