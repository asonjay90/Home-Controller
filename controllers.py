from time import sleep
from subprocess import call
import json


class Controllers(object):
    
    def __init__(self, setup):
        
        buttons = setup.load_remotes()
        self.HDMI_BUTTONS = buttons['HDMI']
        self.GPIO_BUTTONS = buttons['GPIO']
        self.HUE_BUTTONS = buttons['HUE']
        self.IR_BUTTONS = buttons['IR']
        self.GPIO_DEVICE = setup.setup_gpio(self.GPIO_BUTTONS)
        self.HDMI_DEVICE = setup.setup_cec()
        self.HUE_DEVICE = setup.setup_hue()
        self.SQL = setup.db_init()
    
    def GPIO_command(self, device, command):
        if command in self.GPIO_BUTTONS[device]:
            pins = self.GPIO_BUTTONS[device][command]
            current_values = eval(self.SQL.select_query('GPIO', device))
            for pin in pins:
                self.GPIO_DEVICE.output(int(pin), self.GPIO_DEVICE.LOW)
                sleep(.3)
                self.GPIO_DEVICE.output(int(pin), self.GPIO_DEVICE.HIGH)
                sleep(.3)
            if device == 'ceiling':
                if command not in ['allon', 'alloff']:    
                    current_values[command] = not current_values[command]
                    self.SQL.update_query('GPIO', device, current_values)
                    return [str(current_values), 200]
                if command == 'allon':
                    for light in current_values:
                        current_values[light] = True
                    return [str(current_values), 200]
                else:
                    for light in current_values:
                        current_values[light] = False
                    return [str(current_values), 200]
            current_values[command] = not current_values[command]
            self.SQL.update_query('GPIO', device, current_values)
            return [str(current_values), 200]
        return ["Unknown Command!", 400]

    def Hue_command(self, command):
        if command in self.HUE_BUTTONS:
            action = self.HUE_BUTTONS[command]
            if 'bulb2' in action:
                self.HUE_DEVICE.set_light([1,3], action['all'])
                self.HUE_DEVICE.set_light(2, action['bulb2'])
            else:
                self.HUE_DEVICE.set_light([1,2,3], action['all'])
            return ["Success!", 200]
        return ["Unknown Command!", 400]
    
    def HDMI_command(self, command):
        if command in self.HDMI_BUTTONS:
            commands = self.HDMI_BUTTONS[command]
            for action in commands:
                to_send = self.HDMI_DEVICE.CommandFromString(action)
                self.HDMI_DEVICE.Transmit(to_send)
                sleep(.1)
            return ["Success!", 200]
        return ["Unknown Command!", 400]

    def IR_command(self, device, command):
        if command in self.IR_BUTTONS[device]:
            action = self.IR_BUTTONS[device][command]
            cmd = "irsend SEND_ONCE " + device + " " + action
            call(cmd, shell=True)
            # Update databse with new vallues
            current_values = eval(self.SQL.select_query('IR', device))
            if device == 'fan':
                if command == 'speed':
                    if current_values['speed'] == 1:
                        current_values['speed'] = 3
                    else: current_values['speed'] -= 1
                else: current_values[command] = not current_values[command]
            if device == 'receiver':
                if command == 'power':
                    current_values[command] = not current_values[command]
                elif command not in ['vol_up', 'vol_down']:
                    current_values['input'] = command
            self.SQL.update_query('IR', device, current_values)
            
            return [str(current_values), 200]
        return ["Unknown Command!", 400]

    def reload_devices(self, setup):
        self.__init__(setup)
        return ["Success!", 200]

    def keep_alive(self):
	return 'True', 200    


    def get_status(self, interface, device):
        status = self.SQL.select_query(interface, device)
        return status, 200
     
    def return_status(self, API, status):
        response = API.make_response(status[0])
        code = status[1]
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response, code

