import time
import random

def generate_pin_from_user(pin_length):
    while True:
        user_input = input(f"Enter {pin_length}-digit PIN: ")
        if len(user_input) == pin_length and user_input.isdigit():
            yield user_input
        else:
            print(f"Invalid input. Please enter a {pin_length}-digit PIN.")

def run_ms_simulator(delay, callback, stop_event, publish_event, settings):
    pin_length = 4
    for value in generate_pin_from_user(pin_length):
        time.sleep(delay)
        callback(value, publish_event, settings)
        if stop_event.is_set():
            break

