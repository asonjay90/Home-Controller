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
import yaml

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
        self.lib = None
        self.status_message = None
        self.status_code = None
        #setup devices
        self.load_remotes()
        self.setup_cec()
        self.setup_gpio()
        self.setup_hue()


    def get_status_message(self):
        """Fetches the status message of last run command.

        Rerurns:
            A string with a success or failure message
        """
        return self.status_message


    def get_status_code(self):
        """Fetches the HTTP status code of last run command.

        Rerurns:
            A string with a HTTP status code
        """
        return self.status_code


    def get_status_hue(self):
        """ Check if any bulb is currently on
            If one is on, consider them all on

        Returns:
            bool of power status
        """
        status = False
        # Always assume the bulbs are off
        for bulb in self.hue_bulbs:
            if bulb.on == True:
                status = True
                break
        return status


    def load_remotes(self):
        """ (re)Loads YAML containing all the commands for the remotes.

        """
        try:
            with open('remotes.yaml', 'r') as da_file:
                remotes = yaml.load(da_file)
            self.HDMI = remotes['HDMI']
            self.CEILING = remotes['CEILING']
            self.HUE = remotes['HUE']

            # return successfull execution
            self.status_message = "INFO - Remotes reloaded successfully"
            self.status_code = 200
            print self.status_message

        except RuntimeError as exc:
            # return unsuccessfull execution with error
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 501
            print self.status_message
            return 0
            

    def setup_cec(self):
        """Creates config and opens connect to CEC (HDMI) adapter
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
        """Sets up RaspberryPi GPIO pins
        """
        # Set up GPIO using BCM GPIO pin numbers
        GPIO.setmode(GPIO.BOARD)
        # Set relay pins as output
        for switch in self.CEILING:
            for pin in self.CEILING[switch]['commands']:
                GPIO.setup(int(pin), GPIO.OUT, initial=GPIO.HIGH)
        # Supress warnings
        GPIO.setwarnings(False)
        print "GPIO setup successfully"


    def setup_hue(self):
        """Connects to Hue bridge and creates object for bulbs
        """
        # Set up Philips hue lights
        self.hue = Bridge('10.0.0.103')
        #hue.connect() # uncomment if running for first time
        self.hue_bulbs = self.hue.lights
        print "HUE setup successfully"


    def process_command(self, device, action, option=None):
        """Proccesses command from API and runs corresponding method

        Args:
            device: A string of device to control
            action: A string of an action for that device
        """
        self.device = device.lower()
        action = action.lower()

        if device == 'ceiling':
            self.control_celing(action)
        elif device == 'hue':
            print option
            if option != None:
                self.control_hue(action, option)
            else:
                self.control_hue(action)
        elif device == 'av':
            self.control_hdmi(action)
        elif device == 'remotes':
            self.load_remotes()
        elif device == 'party':
            self.control_party(action)
        else:
            self.status_message = "ERROR - " + device + " not found"
            self.status_code = 501
            print self.status_message


    def control_celing(self, button):
        """Control ceiling lights using GPIO

        Args:
            button: A string of the light name in remotes.yaml
        """
        try:
            if button in self.CEILING:
                # Set pins to toggle
                pins = self.CEILING[button]['commands']
                for pin in pins:
                    # Toggle button
                    GPIO.output(int(pin), GPIO.LOW)
                    sleep(.1)
                    GPIO.output(int(pin), GPIO.HIGH)
                    if button == 'allon' or button == 'alloff':
                        sleep(.5)
                # return successfull execution
                self.status_message = "INFO - '" + button + "' on device '" + \
                                     self.device + "' completed successfully"
                self.status_code = 200
                print self.status_message

        except RuntimeError as exc:
            # return unsuccessfull execution with error
            self.status_message = "ERROR - " + str(exc)
            self.status_code = 501
            print self.status_message
            return 0


    def control_hue(self, action, bri=254):
        """Control the Philips hue bulbs using phue library

        Args:
            action: A string of a command to perform
        """
        try:
            if action in self.HUE:
                cmd = self.HUE[action]
                if 'bulb2' in cmd:
                    cmd2 = cmd.pop('bulb2', None)
                    self.hue.set_light([1,3], cmd)
                    self.hue.set_light(2, cmd2)
                else:
                    self.hue.set_light([1,2,3], cmd)
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


    def control_hdmi(self, action):
        """Control devices using HDMI and libcec

        Args:
            action: sting of action to perform via cec HDMI
        """
        try:
            if action in self.HDMI:
                commands = self.HDMI[action]['commands']
                for command in commands:
                    to_send = self.lib.CommandFromString(command)
                    self.lib.Transmit(to_send)
                    sleep(.1)

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


    def control_party(self, action):
        """Controls the state of party mode

        Args:
            action: A string of 'on' or 'off'
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

