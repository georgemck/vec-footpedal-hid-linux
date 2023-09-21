# vec-footpedal-hid-linux
A quick and dirty implementation of mapping for a VEC footpedal HID device on Linux

## Features
* Allows remapping of a VEC footpedal to any keys.
* Automatically finds the footpedal.

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
5. `/dev/input/event*`

## Other Resources
