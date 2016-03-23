"""Control Module for my apt

This is used to create a remote controller instance to
control all the IOT devices in my apt. It is currently
imported into the Flask API server for easy use via the web.

Created by Jason Simon - Q1 2016

"""

from subprocess import call
from time import sleep
import urllib2
from phue import Bridge
import RPi.GPIO as GPIO
import cec

class Controller:
    """ This class is used as a remote to control my apt.

    Use the proccess_command method to control the device and
    send an action to perform. This will trigger the corresponding
    method to perfrom the desired action. That method will also
    set the status_message and status_code to be used in with an
    RESTful API such as Flask.

    """
    def __init__(self):
        #setup attributes
        self.device = None
        self.hue = None
        self.hue_bulbs = None
        self.switches = None
        self.lib = None
        self.status_message = None
        self.status_code = None
        #setup devices
        self.setup_cec()
        self.setup_gpio()
        self.setup_hue()


    def get_status_message(self):
        """Fetches the status message of last run command.

        Args:
            None

        Rerurns:
            A string with a success or failure message
        """
        return self.status_message


    def get_status_code(self):
        """Fetches the HTTP status code of last run command.

        Args:
            None

        Rerurns:
            A string with a HTTP status code
        """
        return self.status_code


    def setup_cec(self):
        """Creates config and opens connect to CEC (HDMI) adapter

        Args:
            None
        Returns:
            None
        """
        # Set up CEC config
        cecconfig = cec.libcec_configuration()
        cecconfig.strDeviceName = "aptcontroller"
        cecconfig.bActivateSource = 0
        cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
        cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT
        # Create, Detect, and Open adapter
        self.lib = cec.ICECAdapter.Create(cecconfig)
        adapters = self.lib.DetectAdapters()
        self.lib.Open(adapters[0].strComName)
        print "CEC setup successfully"


    def setup_gpio(self):
        """Sets up RaspberryPi GPIO pins and create dict of switches/pins

        Args:
            None
        Returns:
            None
        """
        # Set pin layout for GPIO and celing lights
        self.switches = {
            'row1':3,    # Light row 1 = pin 3
            'row2':5,    # Light row 2 = pin 5
            'row3':7,    # Light row 3 = pin 7
            'row4':11,   # Light row 4 = pin 11
            'bri':13,    # Brighten Lights = pin 13
            'dim':15,    # Dim Lights = pin 15
            'allon':19,  # All lights on = pin 19
            'alloff':21  # All lights off = pin 21
            }
        # Set up GPIO using BCM GPIO pin numbers
        GPIO.setmode(GPIO.BOARD)
        # Set relay pins as output
        for switch in self.switches:
            GPIO.setup(self.switches[switch], GPIO.OUT, initial=GPIO.HIGH)
        # Supress warnings
        GPIO.setwarnings(False)
        print "GPIO setup successfully"


    def setup_hue(self):
        """Connects to Hue bridge and creates object for bulbs

        Args:
            None
        Returns:
            None
        """
        # Set up Philips hue lights
        self.hue = Bridge('10.0.0.103')
        #hue.connect() # uncomment if running for first time
        self.hue_bulbs = self.hue.lights
        print "HUE setup successfully"


    def process_command(self, device, action):
        """Proccesses command from API and runs proper method

        Args:
            device: A string of device to control
            action: A string of an action for that device
        Returns:
            None
        """
        self.device = device.lower()
        action = action.lower()

        if device == 'ceiling':
            self.control_celing(action)
        elif device == 'hue':
            self.control_hue(action)
        elif device == 'av':
            self.control_hdmi(action)
        elif device =='plex':
            self.control_plex(action)
        elif device == 'party':
            self.control_party(action)
        else:
            self.status_message = "ERROR - " + device + " not found"
            self.status_code = 501
            print self.status_message


    def control_celing(self, light):
        """Control ceiling lights using GPIO

        Args:
            light: A string of the light name in the switch dict
        Returns:
            None
        """
        try:
            # Set pin to toggle
            pin = self.switches[light]
            # To ensure action happens to all lights, press dim or bri before
            if light == 'allon':
                self.control_celing('bri')
                sleep(.5)
            elif light == 'alloff':
                self.control_celing('dim')
                sleep(.5)
            # Toggle button
            GPIO.output(pin, GPIO.LOW)
            sleep(.1)
            GPIO.output(pin, GPIO.HIGH)
            # return successfull execution
            self.status_message = "INFO - '" + light + "' on device '" + \
                                 self.device + "' completed successfully"
            self.status_code = 200
            print self.status_message

        except RuntimeError as exc:
            # return unsuccessfull execution with error
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 501
            print self.status_message
            return 0


    def control_hue(self, action):
        """Control the Philips hue bulbs using phue library

        Args:
            action: A string of a command to perform
        Returns:
            None
        """
        try:
            if action == 'power':
                status = False
                # Check if any bulb is currently on
                # If one is on, consider them all on
                for bulb in self.hue_bulbs:
                    if bulb.on == True:
                        status = True
                        break
                # Turn off bulbs
                if status == True:
                    self.hue.set_light([1, 2, 3], 'on', False)
                # Turn on bulbs
                else:
                    command = {'transitiontime' : 25, 'on' : True, 'bri' : 254}
                    self.hue.set_light([1, 2, 3], command)
            # Preset 'Energize'
            elif action == 'preset1':
                for bulb in self.hue_bulbs:
                    bulb.on = True
                    bulb.transitiontime = 1
                    bulb.brightnesss = 254
                    bulb.colortemp_k = 6410
            # Preset 'Sunset'
            elif action == 'preset2':
                for bulb in self.hue_bulbs:
                    bulb.on = True
                    bulb.transitiontime = 1
                    bulb.brightnesss = 254
                    bulb.colortemp_k = 2170
                #set middle bulb
                self.hue_bulbs[1].xy = [0.6349, 0.3413]
            # Preset 'Love Shack'
            elif action == 'preset3':
                for bulb in self.hue_bulbs:
                    bulb.on = 1
                    bulb.brightness = 254
                    #bulb.colormode = 'hs'
                    bulb.hue = 53498
                    bulb.saturation = 254
                    bulb.color_temperature = 200
                #set middle bulb
                self.hue_bulbs[1].hue = 48401

            else:
                # return unsuccessful execution
                self.status_message = "ERROR - '" + action + "' on '" + \
                                     self.device + "' not found"
                self.status_code = 501
                print self.status_message
                return
            # return successfull exectution
            self.status_message = "INFO - '" + action + "' on '" + \
                                  self.device + "' completed successfully"
            self.status_code = 200
            print self.status_message

        except RuntimeError as exc:
            # return unsuccesfull execution with error
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 500
            print self.status_message


    def control_party(self, action):
        """Controls the state of party mode

        Args:
            action: A string of 'on' or 'off'
        Returns:
            None
        """
        try:
            if action == 'on':
                cmd = "sudo python /home/jason/server/party_mode.py &"
                call(cmd, shell=True)

            elif action == 'off':
                cmd = "ps aux | " + \
                      "grep party_mode.py | " + \
                      "awk '{ print $2 }' | " + \
                      "sudo xargs kill"
                call(cmd, shell=True)
                self.control_hue('preset1')
                self.control_hue('power')

            else:
                # return unsuccessful execution
                self.status_message = "ERROR - '" + action + "' on '" + \
                                     self.device + "' not found"
                self.status_code = 501
                print self.status_message
                return
            # return successfull exectution
            self.status_message = "INFO - '" + action + "' on '" + \
                                 self.device + "' completed successfully"
            self.status_code = 200
            print self.status_message

        except RuntimeError as exc:
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 500
            print self.status_message

    def control_hdmi(self, action):
        """Control devices using HDMI and libcec

        Args:
            action: sting of action to perform via cec HDMI
        Returns:
            None
        """
        try:
            if action == 'watchtv':
                tvpower = self.lib.CommandFromString('10:04')
                setinput = self.lib.CommandFromString('1f:82:21:00')

                self.lib.Transmit(tvpower)
                sleep(.1)
                self.lib.Transmit(setinput)

            elif action == 'alloff':
                alloff = self.lib.CommandFromString('1f:36')
                self.lib.Transmit(alloff)

            else:
                # return unsuccessful execution
                self.status_message = "ERROR - '" + action + "' on '" + \
                                     self.device + "' not found"
                self.status_code = 501
                print self.status_message
                return
            # return successfull exectution
            self.status_message = "INFO - '" + action + "' on '" + \
                                 self.device + "' completed successfully"
            self.status_code = 200
            print self.status_message

        except RuntimeError as exc:
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 500
            print self.status_message

    def control_plex(self, action):
        """Control Plex media player

        Args:
            action: string of action to perform
        Returns:
            None
        """
        try:
            if action == 'play':
                response = urllib2.urlopen('http://10.0.0.39:32500/player/playback/play?type=video')
                html = response.read()
                
            elif action == 'pause':
                response = urllib2.urlopen('http://10.0.0.39:32500/player/playback/pause?type=video')
                html = response.read()
                
            elif action == 'skipnext':
                response = urllib2.urlopen('http://10.0.0.39:32500/player/playback/skipNext?type=video')
                html = response.read()
                
            elif action == 'skipprevious':
                response = urllib2.urlopen('http://10.0.0.39:32500/player/playback/skipPrevious?type=video')
                rhtml = response.read()
            
            else:
                # return unsuccessful execution
                self.status_message = "ERROR - '" + action + "' on '" + \
                                     self.device + "' not found"
                self.status_code = 501
                print self.status_message
                return
            # return successfull exectution
            self.status_message = "INFO - '" + action + "' on '" + \
                                 self.device + "' completed successfully"
            self.status_code = 200
            print self.status_message
                
        except RuntimeError as exc:
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 500
            print self.status_message
