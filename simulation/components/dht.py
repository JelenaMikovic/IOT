from simulators.uds import run_uds_simulator
import threading
import time

def uds_callback(humidity, temperature, code):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting uds sumilator")
            uds_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print("uds sumilator started")
        else:
            from sensors.uds import run_uds_loop, UDS
            print("Starting uds loop")
            uds = UDS(settings['pin'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print("uds loop started")
