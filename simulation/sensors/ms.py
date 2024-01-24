import RPi.GPIO as GPIO
import time

class MS(object):
	def __init__(self, R1, R2, R3, R4, C1, C2, C3, C4):
		self.R1 = R1
		self.R2 = R2
		self.R3 = R3
		self.R4 = R4

		self.C1 = C1
		self.C2 = C2
		self.C3 = C3
		self.C4 = C4

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.R1, GPIO.OUT)
		GPIO.setup(self.R2, GPIO.OUT)
		GPIO.setup(self.R3, GPIO.OUT)
		GPIO.setup(self.R4, GPIO.OUT)

		GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	def readLine(self, line, characters):
		GPIO.output(line, GPIO.HIGH)
		if(GPIO.input(self.C1) == 1):
			return (characters[0])
		if(GPIO.input(self.C2) == 1):
			return (characters[1])
		if(GPIO.input(self.C3) == 1):
			return (characters[2])
		if(GPIO.input(self.C4) == 1):
			return (characters[3])
		GPIO.output(line, GPIO.LOW)
	
	def key_press(self, pin_length):
		pin = ""
		while len(pin) < pin_length:
			for line, characters in zip([self.R1, self.R2, self.R3, self.R4], [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]):
				key = self.readLine(line, characters)
				if key:
					pin += key
					print(f"Entered digits: {pin}")
					time.sleep(0.2)        
		return pin
		
	def run_ms_loop(self, delay, callback, stop_event, publish_event, settings):
        pin_length = 4  
        while True:
            pin_entered = self.key_press(pin_length)
            callback(pin_entered, publish_event, settings)
            if stop_event.is_set():
                break
            time.sleep(delay)
