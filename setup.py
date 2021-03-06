from phue import Bridge
import RPi.GPIO as GPIO
import cec
import yaml
import sql
import settings
import os
import glob


class setup_devices(object):
        
    def load_remotes(self):
        """ (re)Loads YAML containing all the commands for the remotes."""

        with open(settings.REMOTES, 'r') as da_file:
            remotes = yaml.load(da_file)
        
        print "Remotes loaded successfully."
        return remotes
        
    def setup_cec(self):
        """Creates config and opens connect to CEC (HDMI) adapter."""
        
        cecconfig = cec.libcec_configuration()
        cecconfig.strDeviceName = "aptcontroller"
        cecconfig.bActivateSource = 0
        cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
        cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT
        # Create, Detect, and Open adapter
        lib = cec.ICECAdapter.Create(cecconfig)
        adapters = lib.DetectAdapters()
        lib.Open(adapters[0].strComName)

        print "CEC setup successfully."
        return lib

    def setup_gpio(self, remotes):
        """Sets up RaspberryPi GPIO pins."""
        # Set up GPIO using BCM GPIO pin numbers
        GPIO.setmode(GPIO.BOARD)
        for device in remotes:
            for switch in remotes[device]:
                for pin in remotes[device][switch]:
                    pin = int(pin)
                    if pin in [24, 26]:
                        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                    else:
                        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        # Supress warnings
        GPIO.setwarnings(False)

        print "GPIO setup successfully."
        return GPIO

    def setup_hue(self):
        """Connects to Hue bridge and creates object for bulbs."""

        hue = Bridge('10.0.0.103')
        #hue.connect() # uncomment if running for first time
        hue_bulbs = hue.lights

        print "HUE setup successfully."
        return hue
   
    def db_init(self):
        """initializes connection and setup database."""
        
        db_setup = sql.Service()
        print "SQL DB setup successfully."
        return db_setup
        
    def setup_temp(self):
        """setup kernal modules and temp readings location."""
        
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        
        print "Temp sensor setup successfully."
        return device_file        
        

