
from formant.sdk.cloud.v2.src.resources.resources import Resources
from formant.sdk.cloud.v2.formant_query_api_client.api.online_devices import online_devices_controller_online

class OnlineDevices(Resources):

    def online(self):
        'See devices online currently'
        client = self._get_client()
        response = online_devices_controller_online.sync_detailed(client=client)
        return response

    def online_async(self):
        'See devices online currently'
        client = self._get_client()
        response = online_devices_controller_online.asyncio_detailed(client=client)
        return response
