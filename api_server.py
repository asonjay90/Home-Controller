#!/usr/bin/python
from flask import Flask, request
from control import Controller
API = Flask(__name__)
CONTROLLER = Controller()

@API.route('/<device>/<action>')
def apt_controller(device, action):
    try:
        brightness = request.args.get('brightness')
        if brightness:
            CONTROLLER.process_command(device, action, option=int(brightness))
        else:
            CONTROLLER.process_command(device, action, option=None)
        # Response
        response = CONTROLLER.get_status_message()
        status = CONTROLLER.get_status_code()
        response = API.make_response(response)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response, status

    except Exception as exc:
        print "ERROR: Execution failed"
        print exc
        # Response
        response = "ERROR - Issue running process_command method \n" + str(exc)
        response = API.make_response(response)
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response, 500


# Run the app, Baby!
if __name__ == '__main__':
    API.run(host='0.0.0.0', port=80, debug=True)
