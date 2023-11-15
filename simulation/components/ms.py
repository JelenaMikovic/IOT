from locks import lock
import threading
import time

def ms_callback(key_pressed):
    t = time.localtime()
    with lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Key pressed: {key_pressed}")

def run_ms(settings, threads, stop_event):
        if settings['simulated']:
            with lock:
                print("Starting MS sumilator")
            from simulators.ms import run_ms_simulator
            ms_thread = threading.Thread(target = run_ms_simulator, args=(2, ms_callback, stop_event))
            ms_thread.start()
            threads.append(ms_thread)
            with lock:
                print("MS sumilator started")
        else:
            from simulation.sensors.ms import run_ms_loop, MS
            with lock:
                print("Starting MS loop")
            ms = MS(R1=settings["R1"], R2=settings["R2"],  R3=settings["R3"],  R4=settings["R4"], C1=settings["C1"], C2=settings["C2"], C3=settings["C3"], C4=settings["C4"])
            ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event))
            ms_thread.start()
            threads.append(ms_thread)
            with lock:
                print("MS loop started")

