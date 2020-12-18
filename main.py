from flask import Flask

import logging
import os

from broker import CfBroker
from openbrokerapi import api



###    Init

port = os.getenv("PORT", 5000)





# print('Start server on 127.0.0.1:'+str(port))
# print('Check the catalog at:')
# print('> curl http://127.0.0.1:'+str(port)+'/v2/catalog -H "X-Broker-API-Version: 2.14"')
# api.serve(CfBroker(), None, port=port)

# Simply start the server
# api.serve(ExampleServiceBroker(), api.BrokerCredentials("", ""))

# or start the server without authentication
# api.serve(ExampleServiceBroker(), None)

# or start the server with multiple authentication
# api.serve(ExampleServiceBroker(), [api.BrokerCredentials("", ""), api.BrokerCredentials("", "")])

# or with multiple service brokers and multiple credentials
# api.serve_multiple([ExampleServiceBroker(), ExampleServiceBroker()], [api.BrokerCredentials("", ""), api.BrokerCredentials("", "")])

# or register blueprint to your own FlaskApp instance
app = Flask(__name__)
# logger = basic_config()  # Use root logger with a basic configuration provided by openbrokerapi.log_util
openbroker_bp = api.get_blueprint(CfBroker(), api.BrokerCredentials("admin", "admin"), logging)
app.register_blueprint(openbroker_bp)
app.run("0.0.0.0", port=port)