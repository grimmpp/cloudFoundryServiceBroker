from cfBroker.applicationSettings import ApplicationSettings
from cfBroker.broker import Broker
from cfBroker.cfClient import CfClient
from cfBroker.server import Server

appSettings = ApplicationSettings()
cfClient = CfClient(appSettings)
cfClient.connect()
cfBroker = Broker(appSettings, cfClient)

server = Server(cfBroker, appSettings)
server.start()