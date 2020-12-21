
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
    UpdateServiceSpec,
    BindDetails,
    Binding,
    UnbindDetails,
    UnbindSpec
)

class PlanManagerCfOrg(ServiceBroker):
    
    PLAN_ID = '3454f984-cc25-4d0c-90ad-967faaf7117d'

    def __init__(self, cfClient):
        self.cfClient = cfClient

    def getPlanId(self) -> str:
        return self.PLAN_ID


    def getServicePlan(self) -> ServicePlan:
        return ServicePlan(
            id=self.PLAN_ID,
            name='CF Admin Access',
            description='This service plan gives admin access to Cloud Foundry.',
            bindable=True
        )

    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:
        pass

    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
        pass

    def update(self,
               instance_id: str,
               details: UpdateDetails,
               async_allowed: bool,
               **kwargs
               ) -> UpdateServiceSpec:
        pass

    def bind(self,
             instance_id: str,
             binding_id: str,
             details: BindDetails,
             async_allowed: bool,
             **kwargs
             ) -> Binding:
        #TODO: create account

        
        pass

    def unbind(self,
               instance_id: str,
               binding_id: str,
               details: UnbindDetails,
               async_allowed: bool,
               **kwargs
               ) -> UnbindSpec:
        #TODO: delete account
        pass