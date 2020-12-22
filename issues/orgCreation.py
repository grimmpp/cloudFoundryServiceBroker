from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings
import json

appSettings = ApplicationSettings()
cfClient = CfClient(appSettings)
cfClient.connect()

orgName = "My cool test org"
# orgId = cfClient.v3.organizations.create(orgName, suspended=False).get('guid')

# Traceback (most recent call last):
# File "C:\Users\User\Documents\Projects\cf-broker\cfBroker\test.py", line 6, in <module>
#     orgId = cfClient.v3.organizations.create('my cool test org', suspended=False).get('guid')
# File "C:\Python38\lib\site-packages\cloudfoundry_client\v3\organizations.py", line 21, in create
#     return super(OrganizationManager, self)._create(data)
# File "C:\Python38\lib\site-packages\cloudfoundry_client\v3\entities.py", line 145, in _create
#     return self._post(url, data=data)
# File "C:\Python38\lib\site-packages\cloudfoundry_client\v3\entities.py", line 100, in _post
#     response = self.client.post(url, json=data, files=files)
# File "C:\Python38\lib\site-packages\cloudfoundry_client\client.py", line 240, in post
#     return CloudFoundryClient._check_response(response)
# File "C:\Python38\lib\site-packages\cloudfoundry_client\client.py", line 263, in _check_response
#     raise InvalidStatusCode(HTTPStatus(response.status_code), body)
# cloudfoundry_client.errors.InvalidStatusCode: UNPROCESSABLE_ENTITY : {"errors": [{"detail": "Unknown field(s): 'suspended'", "title": "CF-UnprocessableEntity", "code": 10008}]}

# https://api.dev.cfdev.sh/v2/info
# {
# name: "Small Footprint PAS",
# build: "2.5.7-build.3",
# support: "https://support.pivotal.io",
# version: 0,
# description: "https://docs.pivotal.io/pivotalcf/2-5/pcf-release-notes/runtime-rn.html",
# authorization_endpoint: "https://login.dev.cfdev.sh",
# token_endpoint: "https://uaa.dev.cfdev.sh",
# min_cli_version: "6.23.0",
# min_recommended_cli_version: "6.23.0",
# app_ssh_endpoint: "ssh.dev.cfdev.sh:2222",
# app_ssh_host_key_fingerprint: "e7:71:85:55:ec:10:59:c9:15:14:1b:b9:04:23:d4:44",
# app_ssh_oauth_client: "ssh-proxy",
# doppler_logging_endpoint: "wss://doppler.dev.cfdev.sh:443",
# api_version: "2.131.0",
# osbapi_version: "2.14",
# routing_endpoint: "https://api.dev.cfdev.sh/routing"
# }

# create org
print("\nCreate org: "+orgName)
result = cfClient.v2.organizations._create(data = {"name": orgName})
print("Result: \n{}".format( json.dumps(result) ))
orgId = result['metadata']['guid']

# delete org
url = "{}/v2/organizations/{}?async=false&recursive=true".format(appSettings['CF_API']['url'], orgId)
print("\nDelete Org:")
print("url: "+ url)
result = cfClient.v2.organizations._delete(url)

# check it
print("\nCheck if org was deleted")
orgNames = []
for org in cfClient.organizations.list(): orgNames.append(org['entity']['name'])
print("Existing Orgs: {}".format(', '.join(orgNames)))

if orgName in orgNames: print("\nORG: '{}' WAS NOT DELETED!!!\n".format(orgName))
else: print("Org '{}' was deleted!".format(orgName))