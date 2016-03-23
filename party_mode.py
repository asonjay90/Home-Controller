#!/usr/bin/python

''' This module is used to simulate a 'Party Mode'
    incase someone actually visits me and I have a
    need to convince them I am hip and have friends.
'''

from phue import Bridge
from time import sleep
import random

def party_mode():
    ''' This function connects the the Hue bridge, turns on
        the lights to full brightness, and then creates an
        infinite loop setting the colors randomly until the
        proccess is killed. If running for the first time
        press button on bridge and run with bridge.connect()
    '''

    bridge = Bridge('10.0.0.103') # Enter bridge IP here.
    command = {'transitiontime' : 0, 'on' : True, 'bri' : 254}
    bridge.set_light([1, 2, 3], command)
    lights = bridge.lights

    while True:
        for light in lights:
            light.xy = [random.random(), random.random()]
            sleep(.1)

if __name__ == '__main__':
    party_mode()
