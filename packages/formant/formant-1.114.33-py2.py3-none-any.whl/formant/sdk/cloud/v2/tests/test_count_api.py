import unittest
from formant.sdk.cloud.v2.src.query_api import QueryAPI
from formant.sdk.cloud.v2.formant_query_api_client.models.count_history_query import (
    CountHistoryQuery,
)
from formant.sdk.cloud.v2.formant_query_api_client.models.count_history_query_type import (
    CountHistoryQueryType,
)
from formant.sdk.cloud.v2.formant_query_api_client.models.active_devices_query import (
    ActiveDevicesQuery,
)
import dateutil.parser as parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
QUERY_API_URL = "https://api.formant.io/v1/queries"


class TestCount(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCount, self).__init__(*args, **kwargs)
        self.client = QueryAPI(email=EMAIL, password=PASSWORD, api_url=QUERY_API_URL)

    def test_count_history(self):

        count_history_query_type = CountHistoryQueryType("data-point")
        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-01-11T02:02:00.000Z")
        count_history_query = CountHistoryQuery(count_history_query_type, start, end)

        response = self.client.count.history(count_history_query)
        self.assertEqual(response.status_code, 200)

    def test_active_devices(self):

        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-01-11T02:02:00.000Z")
        active_devices_query = ActiveDevicesQuery(start, end)

        response = self.client.count.active_devices(active_devices_query)
        self.assertEqual(response.status_code, 200)


unittest.main()
