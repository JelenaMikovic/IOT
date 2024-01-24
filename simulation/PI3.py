from queue import Queue
import threading
from settings import load_settings
from components.ds import run_ds
from components.dl import run_dl
from components.uds import run_uds
from components.db import run_db
from components.pir import run_pir
from components.ms import run_ms
from components.dht import run_dht
from components.b4sd import run_b4sd
from components.rgb import run_rgb
from locks import lock
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def start_threads(settings, threads, stop_event, dl_queue, db_queue):
    # RPIR4
    run_pir(settings["RPIR4"], threads, stop_event)
    # RDHT4
    run_dht(settings["RDHT4"], threads, stop_event)
    # DB
    run_db(settings["BB"], threads, stop_event, db_queue)
    # B4SD
    run_b4sd(settings["B4SD"], threads, stop_event)
    # BIR

    # BRGB
    run_rgb(settings["BRGB"], threads, stop_event)

def user_input_thread(stop_event, dl_queue, db_queue):
    while True:
        try:
            user_action = input()
            if user_action.upper() == "O":
                dl_queue.put(True)
            elif user_action.upper() == "F":
                dl_queue.put(False)
            elif user_action.upper() == "B":
                db_queue.put(True)
        except:
            time.sleep(0.001)
            if stop_event.is_set():
                break

def run_user_input_thread(stop_event, threads, dl_queue, db_queue):
    input_thread = threading.Thread(target = user_input_thread, args=(stop_event, dl_queue, db_queue))
    input_thread.start()
    threads.append(input_thread)

if __name__ == "__main__":
    print('Starting app')
    with lock:
        print("""Menu:
                'O' - turn on DL
                'F' - turn off DL
                'B' - DB """)
    settings = load_settings("simulation/settings.json")
    threads = []
    stop_event = threading.Event()
    dl_queue = Queue()
    db_queue = Queue()
    try:
        start_threads(settings, threads, stop_event, dl_queue, db_queue)
        run_user_input_thread(stop_event, threads, dl_queue, db_queue)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        with lock:
            print('Stopping app')
        for t in threads:
            stop_event.set()
