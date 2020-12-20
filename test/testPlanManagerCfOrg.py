import unittest
from unittest.mock import MagicMock

from openbrokerapi.catalog import ServicePlan
from cfBroker.planManagerCfOrg import PlanManagerCfOrg
from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings
from openbrokerapi.service_broker import ProvisionDetails

class TestPlanManagerCfOrg(unittest.TestCase):

    def setUp(self):
        cfClient = MagicMock()
        self.planManager = PlanManagerCfOrg(cfClient)

    def test_catalog(self):
        servicePlan = self.planManager.getServicePlan()
        self.assertTrue(type(servicePlan) is ServicePlan)
        self.assertEqual('CF Org', servicePlan.name)
        self.assertFalse(servicePlan.bindable)

    def test_prov(self):
        instanceId = '29dcc9ea-629c-4307-b0fb-a0f6c047e788'
        details = ProvisionDetails('service_id', 'plan_id', 'organization_guid', 'space_guid', parameters = {'name': 'test org'})
        self.planManager.provision(instanceId, details, async_allowed=True)

if __name__ == '__main__':
    unittest.main()