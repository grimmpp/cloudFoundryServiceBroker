import unittest
from unittest.mock import MagicMock

from openbrokerapi.catalog import ServicePlan
from cfBroker.planManagerCfOrg import PlanManagerCfOrg
from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings
from openbrokerapi.service_broker import ProvisionDetails, UpdateDetails

class TestPlanManagerCfOrg(unittest.TestCase):

    def setUp(self):
        cfClient = MagicMock()
        self.planManager = PlanManagerCfOrg(cfClient)


    ### test catalog

    def test_catalog(self):
        servicePlan = self.planManager.getServicePlan()
        self.assertTrue(type(servicePlan) is ServicePlan)
        self.assertEqual('CF Org', servicePlan.name)
        self.assertFalse(servicePlan.bindable)


    ### test provisioning

    def test_prov(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = ProvisionDetails('service_id', 'plan_id', 'organization_guid', 'space_guid', parameters = {'name': 'test org'})
        self.planManager.provision(instanceId, details, async_allowed=True)

    def prov_neg(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = ProvisionDetails('service_id', 'plan_id', 'organization_guid', 'space_guid', parameters = {})
        self.planManager.provision(instanceId, details, async_allowed=True)

    def test_prov_neg(self):
        with self.assertRaises(Exception) as context:
            self.prov_neg()
        self.assertTrue('No parameter name is given.' in str(context.exception) )


    ### test deprovisioning

    def test_deprov(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        self.planManager.deprovision(instanceId, details = {}, async_allowed=True)

    ### test updates

    def test_rename_org(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = UpdateDetails('service_id', self.planManager.getPlanId(), {'name': 'new org name'})
        self.planManager.update(instanceId, details, async_allowed = True)

    def test_change_quota(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = UpdateDetails('service_id', self.planManager.getPlanId(), {'quota': 'default'})
        self.planManager.update(instanceId, details, async_allowed = True)

    def test_change_nothing(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = UpdateDetails('service_id', self.planManager.getPlanId(), {})
        self.planManager.update(instanceId, details, async_allowed = True)


if __name__ == '__main__':
    unittest.main()