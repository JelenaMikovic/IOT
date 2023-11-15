from locks import lock
import threading
import time

def dht_callback(humidity, temperature):
    t = time.localtime()
    with lock: 
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            with lock: 
                print("Starting DHT sumilator")
            from simulators.dht import run_dht_simulator
            dht_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            with lock: 
                print("DHT sumilator started")
        else:
            from simulation.sensors.dht import run_dht_loop, DHT
            with lock: 
                print("Starting DHT loop")
            dht = DHT(settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            with lock: 
                print("DHT loop started")
