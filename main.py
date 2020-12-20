from applicationSettings import ApplicationSettings
from broker import CfBroker
from cfClient import CfClient
from server import Server

appSettings = ApplicationSettings()
cfClient = CfClient(appSettings)
cfBroker = CfBroker(appSettings, cfClient)

server = Server(cfBroker, appSettings)
server.start()