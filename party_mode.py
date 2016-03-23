#!/usr/bin/python
from phue import Bridge
from time import sleep
import random

b = Bridge('10.0.0.103') # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
b.connect()
lights = b.lights

command =  {'transitiontime' : 0, 'on' : True, 'bri' : 254}
b.set_light([1,2,3], command)
while True:
  for light in lights:
    light.xy = [random.random(),random.random()]
    sleep(.1)
