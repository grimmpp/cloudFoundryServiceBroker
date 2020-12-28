from applicationSettings import ApplicationSettings
from broker import Broker
from cfClient import CfClient
from server import Server

class App():

    def start(self):
        self.printHeadline()

        appSettings = ApplicationSettings()
        cfClient = CfClient(appSettings)
        cfClient.connect()
        cfBroker = Broker(appSettings, cfClient)

        server = Server(cfBroker, appSettings)
        server.start()


    # Headline Generator: https://patorjk.com/software/taag/#p=display&f=Standard&t=Cloud%20%20Foundry%20%20Broker
    def printHeadline(self):
        headline = """\033[94m
          ____ _                 _    _____                     _               ____            _             
         / ___| | ___  _   _  __| |  |  ___|__  _   _ _ __   __| |_ __ _   _   | __ ) _ __ ___ | | _____ _ __ 
        | |   | |/ _ \| | | |/ _` |  | |_ / _ \| | | | '_ \ / _` | '__| | | |  |  _ \| '__/ _ \| |/ / _ \ '__|
        | |___| | (_) | |_| | (_| |  |  _| (_) | |_| | | | | (_| | |  | |_| |  | |_) | | | (_) |   <  __/ |   
         \____|_|\___/ \__,_|\__,_|  |_|  \___/ \__,_|_| |_|\__,_|_|   \__, |  |____/|_|  \___/|_|\_\___|_|   
                                                                       |___/                                  
        \033[0m"""
        print(headline)

if __name__ == '__main__':
    App().start()