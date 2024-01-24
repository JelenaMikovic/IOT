from locks import lock
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from locks import lock
from queue import Queue
from simulators.lcd import run_lcd_simulator

def lcd_callback(temperature,humidity):
    t = time.localtime()
    with lock:
        print("="*20 + "LCD" + "="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Received temperature: {temperature}\n")
        print(f"Received humidity: {humidity}\n")

def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        with lock:
            print("Starting lcd simulator")
        lcd_thread = threading.Thread(target = run_lcd_simulator, args=(10,"test", lcd_callback, stop_event,settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        with lock:
            print("lcd simulator started")
    else:
        from sensors.lcd.LCD1602 import run_lcd_loop, LCD
        with lock:
            print("Starting lcd loop")
        lcd = LCD()
        #lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd,"pisa", 2, stop_event))
        #lcd_thread.start()
        #threads.append(lcd_thread)
        with lock:
            print("lcd loop started")