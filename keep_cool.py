#!/usr/bin/env python
import requests
import sqlite3 as sql
import settings
import json


class thermostat(object):

    def __init__(self):
        current_temp = self.get_temp()
        self.check_temp(current_temp)

    def get_temp(self):
        url = 'http://room-controller/temp'
        response = requests.get(url)
        current_temp = float(response.text)
        return current_temp

    def send_command(self, command):
        url = 'http://room-controller/ac/'
        if command:
            response = requests.post(url + 'pwron')
        else:
            response = requests.post(url + 'pwroff')

    def db_select(self):
        db = sql.connect(settings.DATABASE)
        selected = db.cursor().execute('SELECT state FROM GPIO WHERE id = 3')
        db.commit()
        db.close
        result = eval(json.dumps(selected.fetchone()))
        return result[0]

    def db_update(self, update):
        db = sql.connect(settings.DATABASE)
        update = str(update)
        sql_cmd = 'UPDATE GPIO SET state = "{}" WHERE id = 3'.format(update)
        print sql_cmd
        db.cursor().execute(sql_cmd)
        db.commit()
        db.close()

    def check_temp(self, current_temp):
        
        current_state = eval(self.db_select())
        power = current_state['power']
        thermostat = current_state['thermo']
        min_temp = int(current_state['min'])
        max_temp = int(current_state['max'])
        print "AC", power
        print "Thermo" , thermostat
        print "Min", min_temp
        print "max", max_temp
        print "current", current_temp


        if thermostat:
            print "ENABLED"
            if current_temp >= max_temp:
                print "TEMP > MAX"
                if not current_state['power']:
                    print "AC IS OFF - TURNING ON"
                    self.send_command(True)
                    current_state['power'] = not current_state['power']
                    self.db_update(current_state)

            elif current_temp <= min_temp:
                print "TEMP < MIN"
                if current_state['power']:
                    print "AC IS ON - TURNING OFF" 
                    self.send_command(False)
                    current_state['power'] = not current_state['power']
                    self.db_update(current_state)
            else:
                print "WE ARE IN THE SWEET SPOT"
                pass
        else:
            print "DISABLED"
            if power:
                print "AC IS ON - TURNING OFF"
                self.send_command(False)
                current_state['power'] = not current_state['power']
                self.db_update(current_state)

if __name__ == "__main__":
    thermostat()



