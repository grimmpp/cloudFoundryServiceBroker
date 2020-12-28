from cloudfoundry_client.client import CloudFoundryClient
import requests

import json
import os

from applicationSettings import ApplicationSettings

# https://github.com/cloudfoundry-community/cf-python-client

class CfClient(CloudFoundryClient):
    
    def __init__(self, appSettings: ApplicationSettings):
        self.requests = requests
        self.appSettings = appSettings


    def getBaseUrl(self):
        return self.appSettings['CF_Client']['url']


    def connect(self):
        target_endpoint = self.getBaseUrl()
        username = self.appSettings['CF_Client']['username']
        password = self.appSettings['CF_Client']['password']
        proxy = dict(http=self.appSettings['CF_Client']['HTTP_PROXY'], https=self.appSettings['CF_Client']['HTTPS_PROXY'])
        verifySslCert = not self.appSettings['CF_Client']['skip-ssl-validation']

        super().__init__(target_endpoint, proxy=proxy, verify=verifySslCert)
        self.init_with_user_credentials(username, password)
        print('Connection to Cloud Foundry is established!')
        self.checkCfAPI()


    def checkCfAPI(self):
        url = self.getBaseUrl() + '/v2/info'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = self.requests.get(url, headers=headers, verify=False)
        print(response.raise_for_status()) 
        response = response.json()
        print('Cloud Foundry API Versions: ({})'.format(url) )
        print('* Cloud Controller API Version: {}'.format( response['api_version'] ) )
        print('* Open Service Broker API Version: {}'.format( response['osbapi_version'] ) )


    # needs to be done for testing
    def getAccessToken(self):
        try:
            return self._access_token
        except:
            return ''
            

    def getQuotaByName(self, name: str) -> object:
        # url = self.getBaseUrl() + '/v3/organization_quotas' + '?names=' + name
        url = '{}/v2/quota_definitions?q=name%3A{}'.format(self.getBaseUrl(), name)
        # print("requested path: "+url)

        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self.getAccessToken()}
        # print("headers: "+ json.dumps(headers) )
        response = self.requests.get(url, headers=headers, verify=False)
        print(response.raise_for_status()) 
        response = response.json()
        # print( json.dumps( response ))

        for resource in response['resources']:
            if name == resource['entity']['name']:
                return resource
        return None
        

    def getQuotaGuidByName(self, name: str):
        return self.getQuotaByName(name)['metadata']['guid']


    def setQuota(self, orgGuid: str, quotaGuid:str):
        url = self.getBaseUrl() + '/v2/organizations/' + orgGuid
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self.getAccessToken()}
        data = '{"quota_definition_guid": "'+quotaGuid+'"}'
        
        response = self.requests.put(url, data, headers=headers, verify=False)
        print(response.raise_for_status()) 
        return response.json()


        