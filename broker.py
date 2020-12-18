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

import json
import logging

from cfClient import CfClient

class CfBroker(ServiceBroker):

    def __init__(self):
        self.cfClient = CfClient()

    def catalog(self) -> Union[Service, List[Service]]:
        return Service(
            id='55a0be4a-b831-4420-8680-575f346b1d08',
            name='Cloud Foundry',
            description='service description',
            bindable=False,
            instances_retrievable=True,
            plans=[
                ServicePlan(
                    id='29dcc9ea-629c-4307-b0fb-a0f6c047e788',
                    name='CF Org',
                    description='plan description',
                    bindable=False
                )
            ]
        )

    def provision(self,
                  instance_id: str,
                  details: ProvisionDetails,
                  async_allowed: bool,
                  **kwargs) -> ProvisionedServiceSpec:
        
        if not ('name' in details.parameters):
            raise Exception("No parameter name is given.")

        self.cfClient = CfClient()

        orgGuid = self.cfClient.v3.organizations.create(details.parameters['name'], suspended=False).get('guid')

# ---> small hack: reference to org (org Guid) is stored in dashboard_url field of service instance.
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

        if 'name' in details.parameters:
            orgName = details.parameters.get('name')
            self.cfClient.v3.organizations.update(orgGuid, orgName, suspended=True)
            
        return UpdateServiceSpec(False)