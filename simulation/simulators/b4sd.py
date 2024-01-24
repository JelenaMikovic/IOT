import time 

def run_b4sd_simulator(settings, stop_event, callback, publish_event):
        while True:
            if stop_event.is_set():
                break
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            callback(settings, s, publish_event)
            time.sleep(5)