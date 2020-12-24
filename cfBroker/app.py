from applicationSettings import ApplicationSettings
from broker import Broker
from cfClient import CfClient
from server import Server

class App():

    def start(self):
        appSettings = ApplicationSettings()
        cfClient = CfClient(appSettings)
        cfClient.connect()
        cfBroker = Broker(appSettings, cfClient)

        server = Server(cfBroker, appSettings)
        server.start()


if __name__ == '__main__':
    App().start()