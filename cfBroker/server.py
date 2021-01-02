import logging
from datetime import date, datetime, time

from flask import Flask

from flask import request, abort, current_app
from werkzeug.http import parse_authorization_header

from requests.auth import HTTPBasicAuth

from broker import Broker
from cfClient import CfClient
from applicationSettings import ApplicationSettings
from logger import getLogger

from openbrokerapi import api

from pyctuator.pyctuator import Pyctuator


class Server():
    def __init__(self, broker: Broker, appSettings: ApplicationSettings):
        self.broker = broker
        self.appSettings = appSettings
        self.logger = getLogger(self.appSettings)

    def start(self):
        port = self.appSettings['Broker_API']['port']
        brokerUsername = self.appSettings['Broker_API']['username']
        brokerPassword = self.appSettings['Broker_API']['password']

        self.logger.info('Start server on port: {}'.format(port))
        self.logger.info('Check the catalog at: ')
        self.logger.info('> curl http://127.0.0.1:{}/v2/catalog -H "X-Broker-API-Version: 2.14"'.format(port))
        app = Flask(__name__)

        # register open service broker apu
        loggerForBrokerLib = logging.getLogger()
        loggerForBrokerLib.setLevel(self.appSettings['logging']['level'])
        openbroker_bp = api.get_blueprint(self.broker, api.BrokerCredentials(brokerUsername, brokerPassword), loggerForBrokerLib)
        app.register_blueprint(openbroker_bp)

        # register actuator
        if self.appSettings['actuator']['enabled']: self.__addActuator__(app)
            
        # run web server
        app.run("0.0.0.0", port=port)
        


    # https://pypi.org/project/pyctuator/
    # https://github.com/SolarEdgeTech/pyctuator
    # run spring boot admin app for developer purpose "docker run --rm -p 8080:8080 michayaak/spring-boot-admin:2.2.3-1"
    def __addActuator__(self, app):
        self.logger.info("Start Actuator: ")
        auth = HTTPBasicAuth(self.appSettings['actuator']['sprintBootAdminUsername'], self.appSettings['actuator']['sprintBootAdminPassword'])
        
        pyctuator = Pyctuator(
            app,
            app_name = 'CfBroker',
            app_url = self.appSettings['actuator']['appUrl'],
            pyctuator_endpoint_url = self.appSettings['actuator']['appUrl'] + self.appSettings['actuator']['endpoint'],
            registration_url = self.appSettings['actuator']['sprintBootAdminUrl'],
            registration_auth = auth
        )
        
        pyctuator.register_environment_provider("ApplicationSettings", lambda: self.appSettings)
        
        pyctuator.set_git_info(
            commit = self.appSettings['git-info']['commit'],
            time = self.appSettings['git-info']['time'],
            branch = self.appSettings['git-info']['branch'],
        )

        pyctuator.set_build_info(
            name = self.appSettings['build-info']['name'],
            version = self.appSettings['build-info']['version'],
            time = self.appSettings['build-info']['time']
        )

        # in order to add basic auth to the pyctuator blueprint: remove it from web server, add the basicAuth method, and register it again.
        blueprint = app.blueprints['flask_blueprint']
        del app.blueprints['flask_blueprint']
        # add basic auth
        blueprint.before_request(self.check_blueprint_auth)
        app.register_blueprint(blueprint)

    
    def check_blueprint_auth(self):
        header = parse_authorization_header(request.headers['Authorization'])
        if header == None: header = parse_authorization_header(request.headers['http_Authorization'])
        
        if header == None:
            print('Authorization header not found for authentication')
            return abort(401, 'Authorization header not found for authentication')

        if not (
            header['username'] == self.appSettings['Broker_API']['username'] 
            and header['password'] == self.appSettings['Broker_API']['password']): 
            return abort(401, 'Authorization error')