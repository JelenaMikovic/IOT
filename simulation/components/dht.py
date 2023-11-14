from simulation.simulators.dht import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting uds sumilator")
            uds_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print("uds sumilator started")
        else:
            from simulation.sensors.dht import run_uds_loop, DHT
            print("Starting uds loop")
            dht = DHT(settings['pin'])
            dht_thread = threading.Thread(target=run_uds_loop, args=(dht, 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            print("uds loop started")
