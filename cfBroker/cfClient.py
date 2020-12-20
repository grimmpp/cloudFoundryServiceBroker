
from cloudfoundry_client.client import CloudFoundryClient
import requests

import json
import os

from cfBroker.applicationSettings import ApplicationSettings

class CfClient(CloudFoundryClient):
    
    def __init__(self, appSettings: ApplicationSettings):
        self.appSettings = appSettings

        target_endpoint = appSettings['CF_API']['url']
        username = appSettings['CF_API']['username']
        password = appSettings['CF_API']['password']
        proxy = dict(http=appSettings['CF_API']['HTTP_PROXY'], https=appSettings['CF_API']['HTTPS_PROXY'])
        verifySslCert = not appSettings['CF_API']['skip-ssl-validation']

        super().__init__(target_endpoint, proxy=proxy, verify=verifySslCert)
        self.init_with_user_credentials(username, password)


    def getQuotaByName(self, name: str) -> object:
        url = self.appSettings['CF_API']['url'] + '/v3/organization_quotas' + '?names=' + name
        # print("requested path: "+url)

        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self._access_token}
        # print("headers: "+ json.dumps(headers) )
        response = requests.get(url, headers=headers, verify=False).json()
        # print( json.dumps( response ))

        for resource in response['resources']:
            if name == resource['name']:
                return resource
        return None
        

    def getQuotaGuidByName(self, name: str):
        return self.getQuotaByName(name)['guid']


    def setQuota(self, orgGuid: str, quotaGuid:str):
        url = self.appSettings['CF_API']['url'] + '/v2/organizations/' + orgGuid
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self._access_token}
        data = '{"quota_definition_guid": "'+quotaGuid+'"}'
        return requests.put(url, data, headers=headers, verify=False).json()


        