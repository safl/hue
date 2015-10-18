#!/usr/bin/env python
from keylistener import KeyListener
from hue import Bridge, states

def main():

    bridge = "192.168.1.4"
    username = "114c60782a10a3df2f8c82281afdcbef"

    # Mapping a numbering to whatever numerical
    # id the bridge has given to bulbs/lights.
    bulb2hue = {
        1: 10,
        2: 12,
        3: 11,
        4: 9,
        5: 7,
        6: 8
    }

    # Mapping the numerical keys to keycodes
    keys = {
        "7": 74, "8": 78, "9": 96,
        "4": 73, "5": 77, "6": 81,
        "1": 72, "2": 76, "3": 80, 
        "0": 71, "*": 75, "#": 79,
    }
    # Keyboard device
    dev = "/dev/input/by-id/usb-GASIA_USB_KB_V11-event-kbd"
    
    b = Bridge(bridge, username)    # Construct Bridge object
    l = KeyListener(dev)            # Contruct keyboard listener

                                    # Register callbacks
    l.register_keyPress(keys["0"], lambda event: b.toggle())
  
    for n in xrange(1, 6+1):        # Map 1-6 keypad to toggling lights 1-6
        l.register_keyPress(keys["%d" % n], lambda event: b.toggle(bulb2hue[n]))

    #l.register_keyPress(keys["6"], lambda event: b.set_state(states["Energize"]))
    l.register_keyPress(keys["7"], lambda event: b.set_state(states["Concentrate"]))
    l.register_keyPress(keys["8"], lambda event: b.set_state(states["Reading"]))
    l.register_keyPress(keys["9"], lambda event: b.set_state(states["Relax"]))

    l.register_keyPress(keys["*"], lambda event: b.set_bri(
        {k: v-51 for (k, v) in b.get_bri().items()}
    ))
    l.register_keyPress(keys["#"], lambda event: b.set_bri(
        {k: v+51 for (k, v) in b.get_bri().items()}
    ))
    l.listen()                      # Listen for events

if __name__ == "__main__":
    main()
