
from cloudfoundry_client.client import CloudFoundryClient
import requests

import json
import os

class CfClient(CloudFoundryClient):
    
    def __init__(self):
        self.target_endpoint = 'https://api.dev.cfdev.sh'
        proxy = dict(http=os.environ.get('HTTP_PROXY', ''), https=os.environ.get('HTTPS_PROXY', ''))
        super().__init__(self.target_endpoint, proxy=proxy, verify=False)
        self.init_with_user_credentials('admin', 'admin')


    def getQuotaByName(self, name: str) -> object:
        url = self.target_endpoint + '/v3/organization_quotas' + '?names=' + name
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
        url = self.target_endpoint + '/v2/organizations/' + orgGuid
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self._access_token}
        data = '{"quota_definition_guid": "'+quotaGuid+'"}'
        return requests.put(url, data, headers=headers, verify=False).json()


        