import RPi.GPIO as GPIO
import time

class UDS(object):
    def __innit__(self, TRIG_PIN, ECHO_PIN):
        self.TRIG_PIN = TRIG_PIN
        self.ECHO_PIN = ECHO_PIN
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
    
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

def run_uds_loop(uds, delay, callback, stop_event, publish_event, settings):
    if(settings['name'] == "DUS1"):
        uds.mqtt_client.subscribe("DPIR1")
    if(settings['name'] == "DUS2"):
        uds.mqtt_client.subscribe("DPIR2")
    while True:
        first_distance = uds.get_distance()
        callback(first_distance, publish_event, settings)
        time.sleep(delay)
        second_distance = uds.get_distance()
        callback(second_distance, publish_event, settings)
        if(first_distance < second_distance):
            uds.mqtt_client.publish(settings['name'], "going")
        else:
            uds.mqtt_client.publish(settings['name'], "coming")
        if stop_event.is_set():
                break
        time.sleep(delay)
