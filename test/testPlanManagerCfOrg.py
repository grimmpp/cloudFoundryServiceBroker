import unittest
from unittest.mock import MagicMock

from openbrokerapi.catalog import ServicePlan
from cfBroker.planManagerCfOrg import PlanManagerCfOrg
from cfBroker.cfClient import CfClient
from cfBroker.applicationSettings import ApplicationSettings

class TestPlanManagerCfOrg(unittest.TestCase):

    def setUp(self):
        cfClient = MagicMock()
        self.planManager = PlanManagerCfOrg(cfClient)

    def test_catalog(self):
        servicePlan = self.planManager.getServicePlan()
        self.assertTrue(type(servicePlan) is ServicePlan)
        self.assertEqual('CF Org', servicePlan.name)
        self.assertFalse(servicePlan.bindable)


if __name__ == '__main__':
    unittest.main()