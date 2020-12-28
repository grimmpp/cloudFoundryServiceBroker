import requests
import json
import base64

from applicationSettings import ApplicationSettings

# Example: https://github.com/dattnguyen82/PyUaaClient

class UaaClient():

    tokenService = '/oauth/token'
    baseUrl = ''
    clientId = ''
    clientSecret = ''
    payload = "grant_type=client_credentials"
    authString = ''

    def __init__(self, appSettings: ApplicationSettings):
        self.baseUrl = appSettings['UAA_Client']['baseUrl']
        self.clientId = appSettings['UAA_Client']['clientId']
        self.clientSecret = appSettings['UAA_Client']['clientSecret']
        auth = self.clientId + ':' + self.clientSecret
        self.authString = base64.b64encode(auth)
        self.authString = 'Basic ' + self.authString

    def getToken(self):
        url = self.baseUrl + self.tokenService

        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': self.authString,
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=self.payload, headers=headers)

        access_token = json.loads(response.text)

        return access_token['access_token']