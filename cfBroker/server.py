import logging

from flask import Flask

from broker import Broker
from cfClient import CfClient
from applicationSettings import ApplicationSettings
from logger import getLogger

from openbrokerapi import api


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
        loggerForBrokerLib = logging.getLogger()
        loggerForBrokerLib.setLevel(self.appSettings['logging']['level'])
        openbroker_bp = api.get_blueprint(self.broker, api.BrokerCredentials(brokerUsername, brokerPassword), loggerForBrokerLib)
        app.register_blueprint(openbroker_bp)
        app.run("0.0.0.0", port=port)