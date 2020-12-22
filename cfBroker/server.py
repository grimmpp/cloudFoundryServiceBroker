import logging

from flask import Flask

from cfBroker.broker import Broker
from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings

from openbrokerapi import api


class Server():
    def __init__(self, broker: Broker, appSettings: ApplicationSettings):
        self.broker = broker
        self.appSettings = appSettings

    def start(self):
        port = self.appSettings['Broker_API']['port']
        brokerUsername = self.appSettings['Broker_API']['username']
        brokerPassword = self.appSettings['Broker_API']['password']

        print('Start server on port: {}'.format(port))
        print('Check the catalog at: ')
        print('> curl http://127.0.0.1:{}/v2/catalog -H "X-Broker-API-Version: 2.14"'.format(port))
        app = Flask(__name__)
        openbroker_bp = api.get_blueprint(self.broker, api.BrokerCredentials(brokerUsername, brokerPassword), logging)
        app.register_blueprint(openbroker_bp)
        app.run("0.0.0.0", port=port)