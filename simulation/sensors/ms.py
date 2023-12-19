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

	def key_press(self):
		self.readLine(self.R1, ["1","2","3","A"])
		self.readLine(self.R2, ["4","5","6","B"])
		self.readLine(self.R3, ["7","8","9","C"])
		self.readLine(self.R4, ["*","0","#","D"])

	def run_ms_loop(ms, delay, callback, stop_event, publish_event, settings):
		while True:
			key_pressed = ms.key_press()
			callback(key_pressed, publish_event, settings)
			if stop_event.is_set():
					break
			time.sleep(delay)
