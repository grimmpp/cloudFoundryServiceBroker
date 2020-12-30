from typing import Union, List

from cfClient import CfClient
from logger import getLogger

import uuid

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

class PlanManagerAdminAccount(ServiceBroker):
    
    PLAN_ID = '3454f984-cc25-4d0c-90ad-967faaf7117d'


    def __init__(self, cfClient):
        self.cfClient = cfClient
        self.logger = getLogger(cfClient.appSettings)


    def getPlanId(self) -> str:
        return self.PLAN_ID


    def getUsername(self, instanceId: str):
        return "cf-admin-"+instanceId


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
        return ProvisionedServiceSpec()


    def deprovision(self,
                    instance_id: str,
                    details: DeprovisionDetails,
                    async_allowed: bool,
                    **kwargs) -> DeprovisionServiceSpec:
        return DeprovisionServiceSpec(is_async=False)


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
        username = self.getUsername(instance_id)
        password = uuid.uuid4()
        self.cfClient.createUser(username, password, createAdminUser=True)
        self.logger.info("Created CF Admin User: {} for InstanceId: {} and BindingId: {}".format(username, instance_id, binding_id))
        return Binding(credentials = {"username": username, "password": password, "url": self.cfClient.getBaseUrl()})


    def unbind(self,
               instance_id: str,
               binding_id: str,
               details: UnbindDetails,
               async_allowed: bool,
               **kwargs
               ) -> UnbindSpec:
        username = self.getUsername(instance_id)
        self.cfClient.deleteUser(username)
        self.logger.info("Deleted CF Admin User: {} for InstanceId: {} and BindingId: {}".format(username, instance_id, binding_id))
        return UnbindSpec(is_async=False)