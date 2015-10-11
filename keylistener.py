#!/usr/bin/env python
from __future__ import print_function
from evdev import InputDevice, categorize, ecodes

class Callback(object):
    """Keypress callback interface"""

    def __init__(self):
        pass

    def onKeyUp(self, event):
        pass

    def onKeyDown(self, event):
        pass

    def onKeyHold(self, event):
        pass

    def onKeyPress(self, event):
        pass

class KeyListener(object):
    """Listens on input."""

    def __init__(self, dev):
        self.callbacks = {}
        self.dev = InputDevice(dev)

    def register_callback(self, event_code, callback):
        if event_code not in self.callbacks:
            self.callbacks[event_code] = []

        self.callbacks[event_code].append(callback)

    def register_keyUp(self, event_code, func):
        cb = Callback()
        cb.onKeyUp = func
        self.register_callback(event_code, cb)

    def register_keyDown(self, event_code, func):
        cb = Callback()
        cb.onKeyDown = func
        self.register_callback(event_code, cb)

    def register_keyHold(self, event_code, func):
        cb = Callback()
        cb.onKeyHold = func
        self.register_callback(event_code, cb)

    def register_keyPress(self, event_code, func):
        cb = Callback()
        cb.onKeyPress = func
        self.register_callback(event_code, cb)

    def listen(self):

        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY and event.code in self.callbacks:

                for callback in self.callbacks[event.code]: # Dispatch
                    if event.value == 0:
                        callback.onKeyUp(event)
                        callback.onKeyPress(event)
                    elif event.value == 1:
                        callback.onKeyDown(event)
                    elif event.value == 2:
                        callback.onKeyHold(event)
                    else:
                        print("HUH!?")

if __name__ == "__main__":

    l = KeyListener("/dev/input/by-id/usb-GASIA_USB_KB_V11-event-kbd")
    l.register_keyUp(71, lambda event: print(event))
    l.listen()
