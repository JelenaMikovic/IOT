import RPi.GPIO as GPIO
import time

class UDS(object):
    def __innit__(self, TRIG_PIN, ECHO_PIN):
        self.TRIG_PIN = TRIG_PIN
        self.ECHO_PIN = ECHO_PIN

    
    def get_distance(self):
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance

def run_uds_loop(uds, delay, callback, stop_event):
		while True:
			distance = uds.get_distance()
			callback(distance)
			if stop_event.is_set():
					break
			time.sleep(delay)
