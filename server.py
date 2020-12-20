import logging

from flask import Flask

from broker import CfBroker
from cfClient import CfClient
from applicationSettings import ApplicationSettings
from openbrokerapi import api

class Server():
    def init(self, cfBroker: CfBroker, appSettings: ApplicationSettings):
        self.cfBroker = cfBroker
        self.appSettings = appSettings

    def start(self):
        port = self.appSettings['Broker_API']['port']
        brokerUsername = self.appSettings['Broker_API']['username']
        brokerPassword = self.appSettings['Broker_API']['password']

        print('Start server on port: %' % (port))
        print('Check the catalog at: ')
        print('> curl http://127.0.0.1:%/v2/catalog -H "X-Broker-API-Version: 2.14"' % port)
        app = Flask(__name__)
        openbroker_bp = api.get_blueprint(self.cfBroker, api.BrokerCredentials(brokerUsername, brokerPassword), logging)
        app.register_blueprint(openbroker_bp)
        app.run("0.0.0.0", port=port)