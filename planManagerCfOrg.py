
from typing import Union, List

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
    
    PLAN_ID_CF_ORG = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'

    def __init__(self, cfClient):
        self.cfClient = cfClient


    def getPlanId(self) -> str:
        return self.PLAN_ID_CF_ORG


    def getServicePlan(self) -> ServicePlan:
        return ServicePlan(
            id=self.PLAN_ID_CF_ORG,
            name='CF Org',
            description='plan description',
            bindable=False
        )


    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:

        if not ('name' in details.parameters):
            raise Exception("No parameter name is given.")

        orgGuid = self.cfClient.v3.organizations.create(details.parameters['name'], suspended=False).get('guid')

# ---> small hack: reference to org (org Guid) is stored in dashboard_url field of service instance.
# can be put in open service broker v2.16 through metadata field
        return ProvisionedServiceSpec(dashboard_url=orgGuid)


    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
                    
        serviceInstance = self.cfClient.v3.service_instances.get(instance_id)
        orgGuid = serviceInstance.get("dashboard_url")

        self.cfClient.v3.organizations.remove(orgGuid)

        return DeprovisionServiceSpec(is_async=False)


    def update(self,
               instance_id: str,
               details: UpdateDetails,
               async_allowed: bool,
               **kwargs
               ) -> UpdateServiceSpec:

        serviceInstance = self.cfClient.v3.service_instances.get(instance_id)
        orgGuid = serviceInstance.get("dashboard_url")

        # Change quota
        if 'quota' in details.parameters:
            quotaName = details.parameters.get('quota')
            quotaGuid = self.cfClient.getQuotaGuidByName(quotaName)
            self.cfClient.setQuota(orgGuid, quotaGuid)

        # Change org name
        if 'name' in details.parameters:
            orgName = details.parameters.get('name')
            self.cfClient.v3.organizations.update(orgGuid, orgName, suspended=True)
            
        return UpdateServiceSpec(False)
