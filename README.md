# vec-footpedal-hid-linux
A quick and dirty implementation of mapping for a VEC footpedal HID device on Linux

## Features
* Allows remapping of a VEC footpedal to any keys.
* Automatically finds the footpedal. Automatically reconnects on disconnection.
* Doesn't require sudo, if you follow these instructions.

## Contributions
* Open PRs and GitHub Issues as you wish!

## Setup/Usage
1. Set permissions so you don't need to run as sudo.
	1. `sudo nano /etc/udev/rules.d/40-footpedal-hid.rules`
	2. Paste in the following contents.
		```
		SUBSYSTEM=="usb", SYSFS{idVendor}=="05f3", MODE="0666"
		SUBSYSTEM=="usb", ATTRS{idVendor}=="05f3", MODE="0666"
		SUBSYSTEM=="input", SYSFS{idVendor}=="05f3", MODE="0666"
		SUBSYSTEM=="input", ATTRS{idVendor}=="05f3", MODE="0666"
		```
	3. Exit `nano` (Ctrl+X, Y, Enter).
	4. `sudo udevadm control --reload` (or reboot)
2. Install Python dependencies: `python3 -m pip install -r ./requirements.txt`
3. Run `python3 vec-footpedal-hid-linux.py`
4. Consider modifying the code to change the mappings.

## Design Technique
1. Run `sudo evtest` with the device plugged in.
2. Select the footpedal with the list.
3. Press and release each button, and record the output, as follows.
```
Event: time 1695265224.178439, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90001
Event: time 1695265224.178439, type 1 (EV_KEY), code 256 (BTN_0), value 1
Event: time 1695265224.178439, -------------- SYN_REPORT ------------
Event: time 1695265224.466374, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90001
Event: time 1695265224.466374, type 1 (EV_KEY), code 256 (BTN_0), value 0
Event: time 1695265224.466374, -------------- SYN_REPORT ------------
Event: time 1695265237.008789, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90002
Event: time 1695265237.008789, type 1 (EV_KEY), code 257 (BTN_1), value 1
Event: time 1695265237.008789, -------------- SYN_REPORT ------------
Event: time 1695265237.336736, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90002
Event: time 1695265237.336736, type 1 (EV_KEY), code 257 (BTN_1), value 0
Event: time 1695265237.336736, -------------- SYN_REPORT ------------
Event: time 1695265241.480220, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90003
Event: time 1695265241.480220, type 1 (EV_KEY), code 258 (BTN_2), value 1
Event: time 1695265241.480220, -------------- SYN_REPORT ------------
Event: time 1695265241.808159, type 4 (EV_MSC), code 4 (MSC_SCAN), value 90003
Event: time 1695265241.808159, type 1 (EV_KEY), code 258 (BTN_2), value 0
Event: time 1695265241.808159, -------------- SYN_REPORT ------------
```
4. Read and understand the output.
	* The `code` is the 3 buttons.
	* 1 is a press, and 0 is a release.
5. `/dev/input/event*`

## Other Resources and Motivation
The following locations didn't really work, so I created this repo.

* https://saulalbert.net/blog/transcription-with-a-foot-pedal-under-linux/
* https://github.com/kostmo/footpedal
	* Formerly: https://code.google.com/archive/p/footpedal/issues/4#c5
