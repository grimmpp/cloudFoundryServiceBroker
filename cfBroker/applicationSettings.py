import yaml
import json
import logging
import os
import git
from logger import getLogger
from flask import Flask

class ApplicationSettings(dict):

    settingsEnvVarMapping=dict()

    def __init__(self):
        # init logging / start with log level 'INFO' until settings are read
        self.logger = getLogger(self, 'INFO')

        fullFilename = os.path.dirname(__file__) + os.sep +  "settings.yml"
        # print("path: "+fullFilename)
        self.logger.info("Load Application Settings from {}".format(fullFilename))

        with open(fullFilename, 'r') as file: self.update( yaml.load(file, Loader=yaml.FullLoader) )

        port = self.setDefaultSetting('Broker_API', 'port', defaultValue=8080, osEnvName='port')
        self.setDefaultSetting('Broker_API', 'usermane', defaultValue='admin')
        self.setDefaultSetting('Broker_API', 'password', defaultValue='admin')
        
        self.setDefaultSetting('CF_Client', 'url')
        self.setDefaultSetting('CF_Client', 'username')
        self.setDefaultSetting('CF_Client', 'password')
        self.setDefaultSetting('CF_Client', 'skip-ssl-validation', False)
        
        self.setDefaultSetting('logging', 'level', defaultValue='INFO')
        self.setDefaultSetting('logging', 'debug-http-requests', defaultValue=False)
        
        self.setDefaultSetting('actuator', 'enabled', defaultValue=False)
        self.setDefaultSetting('actuator', 'appUrl', defaultValue='http://localhost:'+str(port))
        self.setDefaultSetting('actuator', 'endpoint')
        self.setDefaultSetting('actuator', 'sprintBootAdminUrl', defaultValue='http://localhost:8080/instances')
        self.setDefaultSetting('actuator', 'sprintBootAdminUsername')
        self.setDefaultSetting('actuator', 'sprintBootAdminPassword')
        
        self.logger.info("Settings are loaded.")

        self.logger = getLogger(self)
        logLevel = self['logging']['level']
        self.logger.info("Log level '{}' is set.".format(logLevel))
        
        self.setDefaultSetting('git-info', 'branch')
        self.setDefaultSetting('git-info', 'commit')
        self.setDefaultSetting('git-info', 'time')
        self.tryToSetGitInfo()

        self.setDefaultSetting('build-info', 'name')
        self.setDefaultSetting('build-info', 'version')
        self.setDefaultSetting('build-info', 'time')
        self.tryToSetBuildInfo()

        # print( json.dumps(self))


    def setDefaultSetting(self, settingsSection: str, settingName: str, defaultValue="", osEnvName: str=None):
        # if not exists create default env var name separated with dot
        if osEnvName == None: osEnvName="{}.{}".format(settingsSection, settingName)
        # register env var name for usage and map it to the corresponding value from the yml file.
        self.settingsEnvVarMapping["{}.{}".format(settingsSection, settingName)]=osEnvName
        # if settingsSection does not exist create it
        if settingsSection not in self: self[settingsSection] = {}
        # if setting is not available in settings file add it to the dict.
        if settingName not in self[settingsSection]: self[settingsSection][settingName] = defaultValue
        # if there is an environment variable available overwrite the existing entry.
        self[settingsSection][settingName] = os.getenv(osEnvName, self[settingsSection][settingName])
        # return value
        return self[settingsSection][settingName]


    def getListOfEnvVars(self):
        return self.settingsEnvVarMapping.values()


    def getListOfSettingsKeys(self):
        return self.settingsEnvVarMapping.keys()


    def tryToSetGitInfo(self):
        try:
            repo = git.Repo(search_parent_directories=True)
            branch = repo.active_branch.name
            commit = repo.active_branch.commit.hexsha
            committed_datetime = repo.active_branch.commit.committed_datetime
            
            self['git-info']['branch'] = branch
            self['git-info']['commit'] = commit
            self['git-info']['time'] = committed_datetime
            self.logger.info("Git info was loaded (branch: {}, commit: {}".format(branch, commit))
        except Exception:
            self.logger.error("Was not able to get git information.", exc_info=True)


    def tryToSetBuildInfo(self):
        try:
            from packageInfo import package_name, package_version
            self['build-info']['name'] = package_name
            self['build-info']['version'] = package_version
            self['build-info']['time'] = self['git-info']['time']
        except Exception:
            self.logger.error("Was not able to get build information.", exc_info=True)
