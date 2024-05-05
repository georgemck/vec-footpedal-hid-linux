#!/usr/bin/env python3

# TODO: launch automatically
# TODO: argparse option for debug or forcing the device path

from typing import Union
import evdev
import pyautogui
import argparse
import time
from pynput.keyboard import Key, Controller, Listener
from time import sleep
from pynput import keyboard



def hotkeyFunction(txt=None):
	print(txt)

	def on_activate():
		print('Global hotkey activated!')

	def for_canonical(f):
		print("hot key")
		return lambda k: f(l.canonical(k))

	def on_press(key):
		print('> {} ({})'.format(str(key), listener.canonical(key)))

	def on_release(key):
		print('< {} ({})'.format(str(key), listener.canonical(key)))
		if key == Key.esc:
			return False

	with Listener(
		on_press=on_press,
		on_release=on_release) as listener:
			listener.join()

def write(txt=None):
    if isinstance(txt, str):

        kb = Controller()

        for c in txt:
            kb.type(c)
            sleep(0.05)

def click():
	print('click')
	pyautogui.mouseDown()
	time.sleep(0.1)
	pyautogui.mouseUp()

############## Define your actions here ##############
# Common Options (mouse): pyautogui.mouseDown(), pyautogui.mouseUp(), pyautogui.click() [down and up, has issues though]
# Common Options (keeb):  pyautogui.keyDown(), pyautogui.keyUp(), pyautogui.press() [down and up]
# For an action, write the line like this>>> 'LEFT_PRESS': (lambda: pyautogui.write('Hello world!')),
# For no action, write the line like this>>> 'LEFT_RELEASE': (lambda: pyautogui.write('Hello world!')),
button_actions = {

	'LEFT_PRESS': (lambda: click()),
	'MIDDLE_PRESS': (lambda: pyautogui.write('MIDDLE_PRESS!')),
	'RIGHT_PRESS': (lambda: hotkeyFunction('enable keyboard key capture')),
	'UP_RELEASE':(lambda: write('UP_RELEASE!')),

	#IN CASE NEEDED...
	'LEFT_RELEASE': (lambda: pyautogui.write('LEFT_RELEASE!')),
	'MIDDLE_RELEASE': (lambda: pyautogui.write('MIDDLE_RELEASE!')),
	'RIGHT_RELEASE': (lambda: pyautogui.write('RIGHT_RELEASE!')),

	# WORKING FOR REFERENCE
	# 'LEFT_PRESS': (lambda: pyautogui.write('LEFT_PRESS!')),
	# 'MIDDLE_PRESS': (lambda: pyautogui.write('MIDDLE_PRESS!')),
	# 'RIGHT_PRESS': (lambda: pyautogui.write('RIGHT_PRESS!')),
	# 'UP_RELEASE':(lambda: pyautogui.write('UP_RELEASE!')),
	
	# ORIGINAL CODE ASSIGNMENTS
	# 'LEFT_PRESS': (lambda: pyautogui.keyDown('F2')),
	# 'LEFT_RELEASE': (lambda: pyautogui.keyUp('F2')),
	# 'MIDDLE_PRESS': (lambda: pyautogui.click()),
	# 'MIDDLE_RELEASE': None,
	# 'RIGHT_PRESS': (lambda: pyautogui.click()),
	# 'RIGHT_RELEASE': None,
}
#####################################################

# VEC INFINITY-3
VENDOR_ID = 0x05f3
PRODUCT_ID = 0x00ff
VERSION_ID = 0x000A

# Xbox 360 Wireless Receiver (XBOX)
VENDOR_ID = 0x45e
PRODUCT_ID = 0x2a1
VERSION_ID = 0x114

# Logi USB Headset Logi USB Headset
# getting error -> No device found or permission denied. Trying again in 5 seconds...
# VENDOR_ID = 0x46d
# PRODUCT_ID = 0xa8f 
# VERSION_ID = 0x111


DEBUG_MODE = False
RETRY_DELAY_SECONDS = 5

def find_device_path(vendor_id: int, product_id: int, version_id: int) -> Union[str, None]:
	devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
	for device in devices:
		dev_info = device.info

		# if (dev_info.vendor == vendor_id and dev_info.product == product_id and dev_info.version == version_id):

		if (dev_info.vendor == vendor_id and dev_info.product == product_id):
			return device.path

	return None

def get_event_path_for_correct_device() -> str:
	""" Select the right /dev/input/eventX device.
	Returns a file path like '/dev/input/event9'. Retries if device not found.
	"""
	while (event_dev_path := find_device_path(VENDOR_ID, PRODUCT_ID, VERSION_ID)) is None:
		print(VENDOR_ID, PRODUCT_ID, VERSION_ID)
		print(f"No device found or permission denied. Trying again in {RETRY_DELAY_SECONDS} seconds...")
		time.sleep(RETRY_DELAY_SECONDS)

	return event_dev_path

# Trigger Event Codes: LEFT=256, MIDDLE=257, RIGHT=258
trigger_event_codes = { # keys are codes, values are button names
	256: 'LEFT',
	257: 'MIDDLE',
	258: 'RIGHT',
	0: 'UP',
	1: 'LEFT',
	2: 'MIDDLE',
	4: 'RIGHT',
}
# Trigger Event Values: 1=press, 0=release
trigger_event_values = { # keys are codes, values are actions	
	0: 'RELEASE',
	1: 'PRESS',
	2: 'PRESS',
	3: '???',
	4: 'PRESS',
}

def main():
	
	# Get the path to the device's event thingy
	event_path = get_event_path_for_correct_device()
	print(f"Using event path: '{event_path}'")

	# Create an InputDevice object for your HID device
	device = evdev.InputDevice(event_path)
	for event in device.read_loop():
		try:
			print(event)
			if event.type == evdev.ecodes.EV_KEY:
				trigger_event_code = event.code
				trigger_event_value = event.value
				trigger_event_type = event.type
				# print("event","code:"+str(trigger_event_code),"type:"+str(trigger_event_type),"value:"+str(trigger_event_value))

				event_name = trigger_event_codes[trigger_event_value]
				# print(event_name)
				event_event = trigger_event_values[trigger_event_value]
				# print(event_event)

				event_action = f"{event_name}_{event_event}"
				# print(str(event_name) + " " + str(event_event))
				
				action_fn = button_actions[event_action]
				# print(action_fn)

				if action_fn is not None:
					action_fn()
					print(action_fn())

				if DEBUG_MODE:
					print(f"Event: event.type={event.type}, event.code={event.code}, event.value={event.value}, event_name={event_name}, event_event={event_event}, event_action={event_action}")
		
		except Exception as e:
			print(f"Error in loop: {e}")

if __name__ == '__main__':
	while 1:
		print(f"Starting...")

		try:
			main()
		except KeyboardInterrupt:
			break
		except Exception as e:
			print(f"Error: {e}. Restarting...")
