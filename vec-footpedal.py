#!/usr/bin/env python3


import evdev
import pyautogui

VENDOR_ID = 0x05f3
PRODUCT_ID = 0xff
VERSION_ID = 0x100

DEBUG_MODE = True

def get_event_path_for_correct_device() -> str:
	""" Select the right /dev/input/eventX device. """
	return '/dev/input/event9' # FIXME: select the right one automatically

# Trigger Event Codes: LEFT=256, MIDDLE=257, RIGHT=258
# Trigger Event Values: 1=press, 0=release

trigger_event_codes = { # keys are codes, values are button names
	256: 'LEFT',
	257: 'MIDDLE',
	258: 'RIGHT',
}

trigger_event_values = { # keys are codes, values are actions
	1: 'PRESS',
	0: 'RELEASE',
}

# Common Options: pyautogui.click(), pyautogui.keyDown(), pyautogui.keyUp(), pyautogui.press() [down and up]
# For an action, write the line like this -> 'LEFT_PRESS': (lambda: pyautogui.keyDown('F2')),
# For no action, write the line like this -> 'LEFT_RELEASE': None,
button_actions = {
	'LEFT_PRESS': (lambda: pyautogui.keyDown('F2')),
	'LEFT_RELEASE': (lambda: pyautogui.keyUp('F2')),

	'MIDDLE_PRESS': (lambda: pyautogui.click()),
	'MIDDLE_RELEASE': None,

	'RIGHT_PRESS': (lambda: pyautogui.click()),
	'RIGHT_RELEASE': None,
}

def main():
	# Get the path to the device's event thingy
	event_path = get_event_path_for_correct_device()
	print(f"Using event path: '{event_path}'")

	# Create an InputDevice object for your HID device
	device = evdev.InputDevice(event_path)

	for event in device.read_loop():
		try:
			if event.type == evdev.ecodes.EV_KEY:
				trigger_event_code = event.code
				trigger_event_value = event.value

				event_name = trigger_event_codes[trigger_event_code]
				event_event = trigger_event_values[trigger_event_value]

				event_action = f"{event_name}_{event_event}"
				
				action_fn = button_actions[event_action]

				if action_fn is not None:
					action_fn()

				if DEBUG_MODE:
					print(f"Event: event.type={event.type}, event.code={event.code}, event.value={event.value}, event_name={event_name}, event_event={event_event}, event_action={event_action}")
		
		except Exception as e:
			print(f"Error: {e}")

if __name__ == '__main__':
	main()
