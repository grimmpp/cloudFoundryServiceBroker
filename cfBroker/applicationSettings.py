import yaml
import json
import logging
import os
from logger import getLogger

class ApplicationSettings(dict):

    def __init__(self):
        # init logging
        self.logger = logging.getLogger('AppSettings')
        self.logger.setLevel(logging.INFO)

        fullFilename = os.path.dirname(__file__) + os.sep +  "settings.yml"
        # print("path: "+fullFilename)
        self.logger.info("Load Application Settings from {}".format(fullFilename))

        with open(fullFilename, 'r') as file: self.update( yaml.load(file, Loader=yaml.FullLoader) )

        self.setSetting('Broker_API', 'port', 'port', 8080)
        self.setSetting('Broker_API', 'usermane', 'broker_username')
        self.setSetting('Broker_API', 'password', 'broker_password')
        self.setSetting('CF_Client', 'url', 'cf_client_url')
        self.setSetting('CF_Client', 'username', 'cf_client_username')
        self.setSetting('CF_Client', 'password', 'cf_client_password')
        self.setSetting('CF_Client', 'skip-ssl-validation', 'cf_api_skip_ssl_validation', False)
        self.setSetting('logging', 'level', 'logLevel', 'INFO')
        
        self.logger.info("Settings are loaded.")

        getLogger(self)
        logLevel = self['logging']['level']
        self.logger.info("Log level '{}' is set.".format(logLevel))
        
        # print( json.dumps(self))


    def setSetting(self, settingsSection: str, settingName: str, osEnvName: str, defaultValue=""):
        if settingName not in self[settingsSection]: 
            self[settingsSection][settingName] = defaultValue
        self[settingsSection][settingName] = os.getenv(osEnvName, self[settingsSection][settingName])
        