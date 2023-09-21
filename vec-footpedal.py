#!/usr/bin/env python3


import evdev
from evdev import UInput, ecodes as e

VENDOR_ID = 0x05f3
PRODUCT_ID = 0xff
VERSION_ID = 0x100

def get_event_path_for_correct_device() -> str:
	""" Select the right /dev/input/eventX device. """
	return '/dev/input/event9' # FIXME: select the right one automatically

# Define the event code and value to trigger the "enter" key press
trigger_event_code = 258  # Change this to the correct event code (BTN_2)
trigger_event_value = 1   # Change this to the correct event value (1 for press, 0 for release)

# Create an InputDevice object for your HID device
device = evdev.InputDevice('/dev/input/event9')  # Update the path to your device

# Create a UInput object to simulate key presses
ui = UInput()

for event in device.read_loop():
	if event.type == evdev.ecodes.EV_KEY and event.code == trigger_event_code and event.value == trigger_event_value:
		# Triggered event detected, send an "enter" key press
		ui.write(e.EV_KEY, e.KEY_ENTER, 1)
		ui.write(e.EV_KEY, e.KEY_ENTER, 0)
		ui.syn()

		print(f"Triggered event detected: {event.type} {event.code} {event.value}")

