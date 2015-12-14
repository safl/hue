#!/usr/bin/env python
import argparse
import pprint
import beanstalkc

class RetroHub(object):

    def __init__(self):
        self.conn = None

    def connect(self, hostname, port):
        self.conn = beanstalkc.Connection(host=hostname, port=port)

    def put(self, 

def main():
    """Construct command-line interface and setup hub."""

    parser = argparse.ArgumentParser(description='Retro Smart Home event HUB')
    parser.add_argument(
        '--hostname',
        type=str,
        help='Beanstalk hostname',
        required=True
    )
    parser.add_argument(
        '--port',
        type=int,
        help='Beanstalk port',
        required=True
    )
    args = parser.parse_args()
    
    hub = RetroHub()
    hub.connect(args.hostname, args.port)

if __name__ == "__main__":
    main()
