#!/usr/bin/env python
import logging
from keylistener import KeyListener
from hue import Bridge, states

def main():

    bridge = "192.168.1.3"
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
  
    l.register_keyPress(keys["1"], lambda event: b.toggle(bulb2hue[1]))
    l.register_keyPress(keys["2"], lambda event: b.toggle(bulb2hue[2]))
    l.register_keyPress(keys["3"], lambda event: b.toggle(bulb2hue[3]))
    l.register_keyPress(keys["4"], lambda event: b.toggle(bulb2hue[4]))
    l.register_keyPress(keys["5"], lambda event: b.toggle(bulb2hue[5]))
    l.register_keyPress(keys["6"], lambda event: b.toggle(bulb2hue[6]))

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
    logging.basicConfig(filename='retro.log', level=logging.DEBUG)
    try:
        main()
    except Exception as e:
        logging.error("Error: %s" % e) 
