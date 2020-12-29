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


    def getUaaBaseUrl(self):
        return self.appSettings['CF_API_Info']['token_endpoint']


    def getDefaultHeaders(self):
        headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'bearer '+self.getAccessToken()}
        return headers


    def connect(self):
        target_endpoint = self.getBaseUrl()
        username = self.appSettings['CF_Client']['username']
        password = self.appSettings['CF_Client']['password']
        proxy = dict(http=self.appSettings['CF_Client']['HTTP_PROXY'], https=self.appSettings['CF_Client']['HTTPS_PROXY'])
        self.verifySslCert = not self.appSettings['CF_Client']['skip-ssl-validation']

        super().__init__(target_endpoint, proxy=proxy, verify=self.verifySslCert)
        self.init_with_user_credentials(username, password)
        print('Connection to Cloud Foundry is established!')
        self.checkCfAPI()


    def checkCfAPI(self):
        url = self.getBaseUrl() + '/v2/info'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = self.requests.get(url, headers=headers, verify=self.verifySslCert)
        print(response.raise_for_status()) 
        response = response.json()
        self.appSettings['CF_API_Info'] = response
        
        print('UAA Base Url: {}'.format(self.getUaaBaseUrl()))

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

        headers = self.getDefaultHeaders()
        # print("headers: "+ json.dumps(headers) )
        response = self.requests.get(url, headers=headers, verify=self.verifySslCert)
        response.raise_for_status()
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
        headers = self.getDefaultHeaders()
        data = '{"quota_definition_guid": "{id}"}'.format(id=quotaGuid)
        
        response = self.requests.put(url, data, headers=headers, verify=self.verifySslCert)
        response.raise_for_status()
        return response.json()


    def createUser(self, username, password, createAdminUser:bool=False):
        url = "{}/{}".format( self.getUaaBaseUrl(), "Users" )
        headers = self.getDefaultHeaders()
        data = '{{"emails": [{{ "primary": true, "value": "{user}"}}], "name": {{"familyName": "{user}", "givenName": "{user}"}}, "origin": "", "password": "{pwd}", "userName": "{user}"}}'.format(user=username, pwd=password)

        response = self.requests.post(url, data, headers=headers, verify=self.verifySslCert)
        # skip if user already exists
        if (not response.ok and response.status_code != 409): response.raise_for_status()
        uaaUser = response.json()
        
        if ("id" in uaaUser): userId = uaaUser['id']
        else: userId = uaaUser['user_id']

        # create user mapping in cf
        url = "{}/v2/users".format( self.getBaseUrl() )
        data = '{{"guid": "{id}"}}'.format(id=userId)
        response = self.requests.post(url, data, headers=headers, verify=self.verifySslCert)
        cfUser = response.json()
        if (not response.ok and not ('The UAA ID is taken' in cfUser['description'])): response.raise_for_status()

        if createAdminUser: self.addUserToAllAdminGroups(userId)

        print("\nuser was created\n")
        # print(cfUser)
        return cfUser


    def getUaaGroupByName(self, groupName: str):
        url = "{}/Groups?filter=displayName+Eq+%22{}%22".format(self.getUaaBaseUrl(), groupName)
        headers = self.getDefaultHeaders()
        response = self.requests.get(url, headers=headers, verify=self.verifySslCert)
        response.raise_for_status()
        return response.json()['resources'][0]


    adminGroups = ["cloud_controller.admin", "uaa.admin", "scim.read", "scim.write"]
    def addUserToAllAdminGroups(self, userId):
        for adminGrpName in self.adminGroups:
            grpId = self.getUaaGroupByName(adminGrpName)['id']
            self.addUserToAdminGroup(userId, grpId)


    def addUserToAdminGroup(self, userId, groupId):
        url = "{}/Groups/{}/members".format(self.getUaaBaseUrl(), groupId)
        headers = self.getDefaultHeaders()
        data = '{{"origin": "uaa", "type": "USER", "value": "{}" }}'.format(userId)
        response = self.requests.post(url, data, headers=headers, verify=self.verifySslCert)
        # skip if membership already exists
        if (not response.ok and response.status_code != 409): response.raise_for_status()
        return response.json()


    def getUserByUsername(self, username):
        url = "{}/Users?attributes=id,userName&filter=userName+Eq+%22{}%22".format( self.getUaaBaseUrl(), username )
        headers = self.getDefaultHeaders()

        response = self.requests.get(url, headers=headers, verify=self.verifySslCert)
        response.raise_for_status()
        userInfo = response.json()

        return userInfo['resources'][0]


    def deleteUser(self, username):
        userId = self.getUserByUsername(username)['id']

        # delete user in cf
        url = "{}/v2/users/{}?async=false".format(self.getBaseUrl(), userId)
        headers = self.getDefaultHeaders()
        response = self.requests.delete(url, headers=headers, verify=self.verifySslCert)
        # in case of 404 (user does not exist in CF) try to delete it in UAA as well
        if not response.ok and response.status_code != 404: response.raise_for_status()
        
        # delete user in uaa
        url = "{}/Users/{}".format(self.getUaaBaseUrl(), userId)
        response = self.requests.delete(url, headers=headers, verify=self.verifySslCert)
        response.raise_for_status()
        uaaConfirmation = response.json()

        print("\nuser was deleted\n")


