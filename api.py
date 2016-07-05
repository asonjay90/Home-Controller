#!/usr/bin/python

from flask import Flask, request
import controllers
import setup

API = Flask(__name__)
CONTROLLER = controllers.Controllers(setup.setup_devices())

@API.route('/tv/<action>', methods=['GET', 'POST'])
def tv_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.HDMI_command(action)
        return CONTROLLER.return_status(API, status)
    
@API.route('/av/<action>', methods=['GET', 'POST'])
def av_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.IR_command('receiver', action)
        return CONTROLLER.return_status(API, status)
    if request.method == 'GET':
        status = CONTROLLER.get_status('IR', 'receiver')
        return CONTROLLER.return_status(API, status)
    
@API.route('/ceiling/<action>', methods=['GET', 'POST'])
def ceiling_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.GPIO_command('ceiling', action)
        return CONTROLLER.return_status(API, status)

@API.route('/hue/<action>', methods=['GET', 'POST'])
def hue_handler(action):
    status = CONTROLLER.Hue_command(action)
    return CONTROLLER.return_status(API, status)
    
@API.route('/outlet/<action>', methods=['GET', 'POST'])
def outlet_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.GPIO_command(action)
        return CONTROLLER.return_status(API, status)
    
@API.route('/fan/<action>', methods=['GET', 'POST'])
def fan_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.IR_command("fan", action)
        return CONTROLLER.return_status(API, status)
    if request.method == 'GET':
        status = CONTROLLER.get_status('IR', 'fan')
        return CONTROLLER.return_status(API, status)

@API.route('/nexus/<action>', methods=['GET', 'POST'])
def nexus_handler(action):
    if request.method == 'POST':
        status = CONTROLLER.HDMI_command(action)
        return CONTROLLER.return_status(API, status)

@API.route('/ac/<action>', methods=['GET', 'POST'])
def ac_handler(action):
    if request.method == 'POST':
        if action == 'thermostat':
            enable = request.args.get('enable')
            max_temp = request.args.get('max')
            min_temp = request.args.get('min')
            
            status = CONTROLLER.set_thermo(enable, max_temp, min_temp)
            return CONTROLLER.return_status(API, status)

        status = CONTROLLER.GPIO_command('ac', action)
        return CONTROLLER.return_status(API, status)
    if request.method == 'GET':
        values = CONTROLLER.get_status('GPIO', 'ac')
        return CONTROLLER.return_status(API, values)

@API.route('/temp', methods=['GET'])
def temp_handler():
    if request.method == 'GET':
        status = CONTROLLER.get_temp()
        return CONTROLLER.return_status(API, status)

@API.route('/mood/<action>', methods=['GET', 'POST'])
def mood_handler(action):
    pass

@API.route('/reload/', methods=['POST'])
def reload_handler():
    status = CONTROLLER.reload_devices(setup.setup_devices())
    return CONTROLLER.return_status(API, status) 

@API.route('/alive', methods=['GET'])
def keep_alive_handler():
    status = CONTROLLER.keep_alive()
    return CONTROLLER.return_status(API, status)

# Run the app, Baby!
if __name__ == '__main__':
    API.run(host='0.0.0.0', port=80, debug=True, threaded=True)
