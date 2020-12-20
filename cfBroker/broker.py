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

from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings
from cfBroker.planManagerCfOrg import PlanManagerCfOrg

class Broker(ServiceBroker):

    def __init__(self, appSettings: ApplicationSettings, cfClient: CfClient):
        self.appSettings = appSettings
        self.cfClient = cfClient
        self.planManagerCfOrg = PlanManagerCfOrg(self.cfClient)


    def catalog(self) -> Union[Service, List[Service]]:
        return Service(
            id='55a0be4a-b831-4420-8680-575f346b1d08',
            name='Cloud Foundry',
            description='service description',
            bindable=False,
            instances_retrievable=True,
            plans=[
                self.planManagerCfOrg.getServicePlan()
            ]
        )

    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:
    
        if details.plan_id == self.planManagerCfOrg.getPlanId():
            return self.planManagerCfOrg.provision(instance_id, details, async_allowed)
        else:
            return None


    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
        
        if details.plan_id == self.planManagerCfOrg.getPlanId():
            return self.planManagerCfOrg.deprovision(instance_id, details, async_allowed)

        else: 
            return DeprovisionServiceSpec(is_async=False)


    def update(self,
               instance_id: str,
               details: UpdateDetails,
               async_allowed: bool,
               **kwargs
               ) -> UpdateServiceSpec:

        if details.plan_id == self.planManagerCfOrg.getPlanId():
            return self.planManagerCfOrg.update(instance_id, details, async_allowed)
            
        return UpdateServiceSpec(False)