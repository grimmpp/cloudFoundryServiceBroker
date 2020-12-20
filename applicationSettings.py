import yaml
import json
import logging
import os

class ApplicationSettings(dict):

    def __init__(self):
        fullFilename = os.path.abspath(os.getcwd()) + os.sep +  "settings.yml"
        # print("path: "+fullFilename)

        with open(fullFilename, 'r') as file: self.update( yaml.load(file, Loader=yaml.FullLoader) )

        self.setSetting('Broker_API', 'port', 'port', 8080)
        self.setSetting('Broker_API', 'usermane', 'broker_username')
        self.setSetting('Broker_API', 'password', 'broker_password')
        self.setSetting('CF_API', 'url', 'cf_api_url')
        self.setSetting('CF_API', 'username', 'cf_api_username')
        self.setSetting('CF_API', 'password', 'cf_api_password')
        self.setSetting('CF_API', 'skip-ssl-validation', 'cf_api_skip_ssl_validation', False)
        
        # print( json.dumps(self))


    def setSetting(self, settingsSection: str, settingName: str, osEnvName: str, defaultValue=""):
        if settingName not in self[settingsSection]: 
            self[settingsSection][settingName] = defaultValue
        self[settingsSection][settingName] = os.getenv(osEnvName, self[settingsSection][settingName])
        