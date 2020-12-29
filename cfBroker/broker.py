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

import json
import logging

from cfClient import CfClient
from applicationSettings import ApplicationSettings
from planManagerCfOrg import PlanManagerCfOrg
from planManagerAdminAccount import PlanManagerAdminAccount

# Service Broker API Spec.: https://github.com/openservicebrokerapi/servicebroker/blob/master/spec.md#catalog-management

class Broker(ServiceBroker):

    def __init__(self, appSettings: ApplicationSettings, cfClient: CfClient):
        self.appSettings = appSettings
        self.cfClient = cfClient
        self.planManagerCfOrg = PlanManagerCfOrg(self.cfClient)
        self.planManagerAdminAccount = PlanManagerAdminAccount(self.cfClient)

        self.planManagers = [self.planManagerCfOrg, self.planManagerAdminAccount]


    def getPlanManagersByPlanId(self, planId):
        for pm in self.planManagers:
            if pm.getPlanId() == planId: return pm
        return None


    def getListOfServicePlans(self):
        servicePlans = []
        for pm in self.planManagers:
            servicePlans.append(pm.getServicePlan())
        return servicePlans


    def catalog(self) -> Union[Service, List[Service]]:
        return Service(
            id='55a0be4a-b831-4420-8680-575f346b1d08',
            name='Cloud Foundry',
            description='service description',
            bindable=False,
            instances_retrievable=True,
            plans=self.getListOfServicePlans()
        )


    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:
    
        planManager = self.getPlanManagersByPlanId(details.plan_id)
        return planManager.provision(instance_id, details, async_allowed)
        

    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
        
        planManager = self.getPlanManagersByPlanId(details.plan_id)
        if planManager != None:
            return planManager.deprovision(instance_id, details, async_allowed)

        else: 
            return DeprovisionServiceSpec(is_async=False)


    def update(self,
               instance_id: str,
               details: UpdateDetails,
               async_allowed: bool,
               **kwargs
               ) -> UpdateServiceSpec:

        planManager = self.getPlanManagersByPlanId(details.plan_id)
        if planManager != None:
            return planManager.update(instance_id, details, async_allowed)
            
        return UpdateServiceSpec(False)

    def bind(self,
             instance_id: str,
             binding_id: str,
             details: BindDetails,
             async_allowed: bool,
             **kwargs
             ) -> Binding:
        
        planManager = self.getPlanManagersByPlanId(details.plan_id)
        return planManager.bind(instance_id, binding_id, details, async_allowed)


    def unbind(self,
               instance_id: str,
               binding_id: str,
               details: UnbindDetails,
               async_allowed: bool,
               **kwargs
               ) -> UnbindSpec:
        
        planManager = self.getPlanManagersByPlanId(details.plan_id)
        if planManager != None:
            return planManager.unbind(instance_id, binding_id, details, async_allowed)

        return UnbindSpec(is_async=False)