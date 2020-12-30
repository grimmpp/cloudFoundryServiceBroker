from typing import Union, List
import sys, json

from cfClient import CfClient
from logger import getLogger

import openbrokerapi
from openbrokerapi.api import ServiceBroker
from openbrokerapi.catalog import ServicePlan
from openbrokerapi.service_broker import (
    Service,
    ProvisionDetails,
    ProvisionedServiceSpec,
    DeprovisionDetails,
    DeprovisionServiceSpec,
    UpdateDetails,
    UpdateServiceSpec
)

class PlanManagerCfOrg(ServiceBroker):
    
    PLAN_ID = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'

    def __init__(self, cfClient: CfClient):
        self.cfClient = cfClient
        self.logger = getLogger(cfClient.appSettings)


    def getPlanId(self) -> str:
        return self.PLAN_ID


    def getServicePlan(self) -> ServicePlan:
        return ServicePlan(
            id=self.PLAN_ID,
            name='CF Org',
            description='This service plan delivers a Cloud Foundry Organization.',
            bindable=False
        )


    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:

        if not ('name' in details.parameters):
            raise Exception("No parameter name is given.")

        response = self.cfClient.v2.organizations._create(data = {'name': details.parameters['name']})
        orgGuid = response['metadata']['guid']
        self.logger.info("created Org '{}' with OrgId: {} for InstanceId: {}, in OrgId: {} and SpaceId {}".format(
            details.parameters['name'],
            orgGuid, 
            instance_id,
            details.organization_guid,
            details.space_guid))
        # org creation is also done via v2 api in cf cli.
        # there are problems with v3 creating orgs see /issues/orgCreation.py folder.

# ---> small hack: reference to org (org Guid) is stored in dashboard_url field of service instance.
# can be put in open service broker v2.16 through metadata field
        return ProvisionedServiceSpec(dashboard_url=orgGuid)


    def getOrgGuidByServiceInstanceId(self, instance_Id):
        serviceInstance = self.cfClient.v2.service_instances._get('/v2/service_instances/{}'.format(instance_Id))
        orgGuid = serviceInstance['entity']['dashboard_url']
        # serviceInstance = self.cfClient.v3.service_instances.get(instance_id)
        # orgGuid = serviceInstance.get("dashboard_url")
        return orgGuid


    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
                    
        orgGuid = self.getOrgGuidByServiceInstanceId(instance_id)

        # self.cfClient.v3.organizations.remove(orgGuid)
        # there are problems with v3 creating orgs see /issues/orgCreation.py folder.
        url = "{}/v2/organizations/{}?async=false&recursive=true".format(self.cfClient.getBaseUrl(), orgGuid)
        try:
            self.cfClient.v2.organizations._delete(url)
            self.logger.info("Deleted Org with Id: {}".format(orgGuid))
        except Exception as e:
            # delete service instance also if org was manually deleted in advance
            if "The organization could not be found:" not in str(e): raise e
            self.logger.info("OrgId: {} was already deleted!".format(orgGuid))
            

        return DeprovisionServiceSpec(is_async=False)


    def update(self,
               instance_id: str,
               details: UpdateDetails,
               async_allowed: bool,
               **kwargs
               ) -> UpdateServiceSpec:

        orgGuid = self.getOrgGuidByServiceInstanceId(instance_id)

        # Change quota
        if 'quota' in details.parameters:
            quotaName = details.parameters.get('quota')
            quotaGuid = self.cfClient.getQuotaGuidByName(quotaName)
            self.cfClient.setQuota(orgGuid, quotaGuid)
            self.logger.info("Changed quota for OrgId: {} to '{}' with Id: {}.".format(
                orgGuid,
                quotaName,
                quotaGuid))

        # Change org name
        if 'name' in details.parameters:
            orgName = details.parameters.get('name')
            # self.cfClient.v3.organizations.update(orgGuid, orgName, suspended=True)
            self.cfClient.v2.organizations._update(orgGuid, data={'name': orgName})
            self.logger.info("Changed Org name for OrgId: {} to '{}'.".format(
                orgGuid,
                orgName))
            
        return UpdateServiceSpec(False)
