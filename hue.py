#!/usr/bin/env python
import argparse
import httplib
import pprint
import json

resources = [
    "lights", "groups", "config", "schedules",
    "scenes", "sensors", "rules"
]

states = {
    "Relax": {
        "on": True, "hue": 13088, "bri": 144, "sat": 213,
        "ct": 467, "colormode": "xy", "xy": [0.5134, 0.4149]
    },
    "Concentrate": {
        "on": True, "hue": 33848, "bri": 219, "sat": 44,
        "ct": 234, "colormode": "xy", "xy": [0.3693, 0.3695]
    },
    "Energize": {
        "on": True, "hue": 34494, "bri": 203, "sat": 232,
        "ct": 155, "colormode": "xy", "xy": [0.3151, 0.3252]
    },
    "Reading": {
        "on": True, "hue": 15329, "bri": 240, "sat": 121,
        "ct": 343, "colormode": "xy", "xy": [0.4449, 0.4066]
    }
}

class Bridge(object):
    """
    Bridge communication, basic wrapper around GET/PUT with JSON
    payload encoding/decoding and some convience functions for
    reading resources.

    Usage:
    
    b = Bride(bridge, username)

    Reading resources:;

        b.lights()
        b.config()

    And the like...

    read/write attributes::

        b.get("lights", 1, "state") # State of light Nr. 1
        b.put("lights", 1, "state", {"on": False") # Turn light Nr. 1 offf

    """

    def __init__(self, bridge, username):
        self.bridge = bridge
        self.username = username

        for resource in resources: # Bind resource getters b.lights() etc.
            setattr(self, resource, self._get_resource(resource))

    def _get_resource(self, resource):
        return lambda: self.get(resource)

    def get(self, *args):
        """
        Read a resource

        args are the elements of the URI.
        """

        args_txt = "/".join([str(arg) for arg in args])
        
        conn =  httplib.HTTPConnection("%s" % self.bridge)
        url = '/api/%s/%s' % (self.username, args_txt)
        conn.request('GET', url)
        
        res = conn.getresponse().read()
        res_json = json.loads(res)

        return res_json

    def put(self, *args):
        """
        Write to a resource.
        
        First n-1 args is the URL
        Last argument is the payload as DICT
        """

        payload = json.dumps(args[-1])
        args_txt = "/".join([str(arg) for arg in args[:-1]])

        conn =  httplib.HTTPConnection("%s" % self.bridge)
        url = "/api/%s/%s" % (self.username, args_txt)
        conn.request("PUT", url, payload)
        
        res = conn.getresponse()

        return res

    def toggle(self, light=None):
        """Toggle lights on/off"""

        lights = self.lights()
        for l in lights:
            if light and l != str(light):
                continue
            on = lights[l]["state"]["on"]
            self.put("lights", l, "state", {"on": not on})

    def effect_toggle(self, effect="colorloop", light=None):
        """Toggle lights on/off"""

        lights = self.lights()
        for l in lights:
            if light and l != str(light):
                continue
            value = effect if lights[l]["state"]["effect"] == "none" else "none"
            
            self.put("lights", l, "state", {"effect": value})

    def get_bri(self, light=None):
        """Get brightness"""

        lights = self.lights()
        values = {}
        for l in lights:
            if light and l != str(light):
                continue
            values[l] = int(lights[l]["state"]["bri"])

        return values

    def set_bri(self, values=None):
        """
        Set brightness.
        
        @param values Dict formed as {"1": 255, "2": 50}
        """

        for light in values:
            bri = int(values[light])
            bri = 255 if bri > 255 else bri
            bri = 0 if bri < 0 else bri
            self.put("lights", light, "state", {"bri": bri})

    def set_state(self, state, light=None):
        
        lights = self.lights()
        for l in lights:
            if light and l != str(light):
                continue
            self.put("lights", l, "state", state)

def main():
    parser = argparse.ArgumentParser(description='Philips HUE cli')
    parser.add_argument('bridge', type=str, help='Bridge address')
    parser.add_argument('username', type=str, help='Bridge username')
    parser.add_argument('resource', type=str, nargs='+', help="Resource", choices=resources)

    args = parser.parse_args()

    b = Bridge(args.bridge, args.username)  # Setup bridge
    for resource in args.resource:          # Dump resource
        print("%s:" % resource)
        pprint.pprint(b.__dict__[resource]())

if __name__ == "__main__":
    main()
