import json


class ConfigReader():
    def __init__(self):
        self.config = False


    def read_config(self):
        with open('config.json') as cfg:
            self.config = json.loads(cfg.read())

        return self.config


    def get_db_uri(self):
        if not self.config:
            print("Config has not been loaded")
            return False


        db_type = self.config['database']['type']
        db_path = self.config['database']['path']

        return '%s%s' % (db_type, db_path)
