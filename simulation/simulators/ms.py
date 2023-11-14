import time
import random

def generate_values():
        #R1 ["1","2","3","A"])  # R2, ["4","5","6","B"])   #R3, ["7","8","9","C"])   #R4, ["*","0","#","D"])
        keys = ["1","2","3","A","4","5","6","B","7","8","9","C","*","0","#","D"]
        while True:
            yield keys[random.randint(0,len(keys)-1)]


def run_ms_simulator(delay, callback, stop_event):
        for h, t in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(h, t)
            if stop_event.is_set():
                  break
