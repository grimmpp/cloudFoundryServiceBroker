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
import inspect

from cfClient import CfClient
from applicationSettings import ApplicationSettings
from planManagerCfOrg import PlanManagerCfOrg
from planManagerAdminAccount import PlanManagerAdminAccount
from logger import getLogger

# Service Broker API Spec.: https://github.com/openservicebrokerapi/servicebroker/blob/master/spec.md#catalog-management

class Broker(ServiceBroker):

    def __init__(self, appSettings: ApplicationSettings, cfClient: CfClient):
        # set logging
        self.appSettings = appSettings
        self.logger = getLogger(self.appSettings)

        self.cfClient = cfClient
        self.planManagerCfOrg = PlanManagerCfOrg(self.cfClient)
        self.planManagerAdminAccount = PlanManagerAdminAccount(self.cfClient)

        self.planManagers = [self.planManagerCfOrg, self.planManagerAdminAccount]


    def __getPlanManagersByPlanId__(self, planId):
        for pm in self.planManagers:
            if pm.getPlanId() == planId: return pm
        return None


    def __getListOfServicePlans__(self):
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
            plans=self.__getListOfServicePlans__()
        )


    def log(self, logLevel:int, planManager, instanceId, details):
        functionName = inspect.stack()[1].function
        msg = "{funcName} {planName} - InstanceId: {instId}".format(
            funcName=functionName.capitalize(), 
            planName=planManager.getServicePlan().name, 
            instId=instanceId)
        
        if hasattr(details, 'organization_guid'): msg += ", OrgId: {}".format(details.organization_guid)
        if hasattr(details, 'space_guid'): msg += ", SpaceId: {}".format(details.space_guid)

        self.logger.log(logLevel, msg)


    def provision(self,
                instance_id: str,
                details: ProvisionDetails,
                async_allowed: bool,
                **kwargs) -> ProvisionedServiceSpec:
    
        planManager = self.__getPlanManagersByPlanId__(details.plan_id)
        self.log(logging.INFO, planManager, instance_id, details)
        return planManager.provision(instance_id, details, async_allowed)
        

    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
        
        planManager = self.__getPlanManagersByPlanId__(details.plan_id)
        self.log(logging.INFO, planManager, instance_id, details)
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

        planManager = self.__getPlanManagersByPlanId__(details.plan_id)
        self.log(logging.INFO, planManager, instance_id, details)
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
        
        planManager = self.__getPlanManagersByPlanId__(details.plan_id)
        self.log(logging.INFO, planManager, instance_id, details)
        return planManager.bind(instance_id, binding_id, details, async_allowed)


    def unbind(self,
               instance_id: str,
               binding_id: str,
               details: UnbindDetails,
               async_allowed: bool,
               **kwargs
               ) -> UnbindSpec:
        
        planManager = self.__getPlanManagersByPlanId__(details.plan_id)
        self.log(logging.INFO, planManager, instance_id, details)
        if planManager != None:
            return planManager.unbind(instance_id, binding_id, details, async_allowed)

        return UnbindSpec(is_async=False)