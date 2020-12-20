import yaml
import json
import logging
import os

class ApplicationSettings(dict):

    def __init__(self):
        fullFilename = os.path.abspath(os.getcwd()) + os.sep +  "settings.yml"
        print("path: "+fullFilename)

        with open(fullFilename, 'r') as file: self.update( yaml.load(file, Loader=yaml.FullLoader) )

        self.setSetting('Broker_API', 'port', 8080)
        print( json.dumps(self))


    def setSetting(self, settingsSection: str, osEnvName: str, defaultValue):
        if osEnvName not in self[settingsSection]: 
            self[settingsSection][osEnvName] = defaultValue
        self[settingsSection][osEnvName] = os.getenv(osEnvName, self[settingsSection][osEnvName])
        