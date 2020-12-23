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

        # for Cloud Controller API v3
        # mock_resp = self._mock_response(json_data=json.loads('{"pagination": {"total_results": 2,"total_pages": 1,"first": {"href": "https://api.example.org/v3/organization_quotas?page=1&per_page=50"},"last": {"href": "https://api.example.org/v3/organization_quotas?page=1&per_page=50"},"next": null,"previous": null},"resources": [{"guid": "quota-2-guid","created_at": "2017-05-04T17:00:41Z","updated_at": "2017-05-04T17:00:41Z","name": "sancho-panza","apps": {"total_memory_in_mb": 2048,"per_process_memory_in_mb": 1024,"total_instances": 5,"per_app_tasks": 2},"services": {"paid_services_allowed": true,"total_service_instances": 10,"total_service_keys": 20},"routes": {"total_routes": 8,"total_reserved_ports": 4},"domains": {"total_domains": 7},"relationships": {"organizations": {"data": []}},"links": {"self": { "href": "https://api.example.org/v3/organization_quotas/quota-2-guid" }}}]}'))
        # for Cloud Controller API v2
        mock_resp = self._mock_response(json_data=json.loads('{ "total_results": 1, "total_pages": 1, "prev_url": null, "next_url": null, "resources": [ { "metadata": { "guid": "095a6b8c-31a7-4bc0-a11c-c6a829cfd74c", "url": "/v2/quota_definitions/095a6b8c-31a7-4bc0-a11c-c6a829cfd74c", "created_at": "2016-06-08T16:41:39Z", "updated_at": "2016-06-08T16:41:26Z" }, "entity": { "name": "default", "non_basic_services_allowed": true, "total_services": 100, "total_routes": 1000, "total_private_domains": -1, "memory_limit": 10240, "trial_db_allowed": false, "instance_memory_limit": -1, "app_instance_limit": -1, "app_task_limit": -1, "total_service_keys": -1, "total_reserved_route_ports": 0 } } ]}'))
        mock_get.return_value = mock_resp

        self.cfClient.getQuotaByName('default')