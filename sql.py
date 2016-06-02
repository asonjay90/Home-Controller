import sqlite3 as sql
import settings
import json

class Service(object):

    def __init__(self):
        db = self.establish_connection()
        with open(settings.SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
        
    def establish_connection(self):
        connection = sql.connect(settings.DATABASE)
        return connection
        
    def update_query(self, interface, device, update):
        db = self.establish_connection()
        update = str(update)
        db.cursor().execute("UPDATE {} SET state = ? WHERE device = ?".format(interface), (update, device))
        db.commit()
        db.close()

    def select_query(self, interface, device):
        db = self.establish_connection()
        selected = db.cursor().execute("SELECT state FROM {} WHERE device = ?".format(interface), (device,))
        db.commit()
        db.close
        result = eval(json.dumps(selected.fetchone())) 
        return result[0]
