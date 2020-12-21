import unittest
import json
from mock import Mock, patch
from unittest.mock import MagicMock, PropertyMock

from cfBroker.applicationSettings import ApplicationSettings
from cfBroker.cfClient import CfClient

class TestCfClient(unittest.TestCase):

    def setUp(self):
        appSettings = ApplicationSettings()
        self.cfClient = CfClient(appSettings)
        # self.cfClient.requests = MagicMock()

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('cfBroker.cfClient.requests.get')
    def test_GetQuotaByName(self, mock_get):

        mock_resp = self._mock_response(json_data=json.loads('{"pagination": {"total_results": 2,"total_pages": 1,"first": {"href": "https://api.example.org/v3/organization_quotas?page=1&per_page=50"},"last": {"href": "https://api.example.org/v3/organization_quotas?page=1&per_page=50"},"next": null,"previous": null},"resources": [{"guid": "quota-2-guid","created_at": "2017-05-04T17:00:41Z","updated_at": "2017-05-04T17:00:41Z","name": "sancho-panza","apps": {"total_memory_in_mb": 2048,"per_process_memory_in_mb": 1024,"total_instances": 5,"per_app_tasks": 2},"services": {"paid_services_allowed": true,"total_service_instances": 10,"total_service_keys": 20},"routes": {"total_routes": 8,"total_reserved_ports": 4},"domains": {"total_domains": 7},"relationships": {"organizations": {"data": []}},"links": {"self": { "href": "https://api.example.org/v3/organization_quotas/quota-2-guid" }}}]}'))
        mock_get.return_value = mock_resp

        self.cfClient.getQuotaByName('sancho-panza')