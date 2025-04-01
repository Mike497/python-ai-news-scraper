import configparser


class ConfigUtil:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.properties')

    def get_config(self):
        return self.config
