from ..api import RequestService
from ..endpoints import GenericPluralEndpoint


class AssetsEndPoint(GenericPluralEndpoint):
    def __init__(self, request_service: RequestService, display_id=None):
        super(AssetsEndPoint, self).__init__(request_service=request_service)
        self._endpoint = "/api/v2/assets"
        self.resource_key = "assets"
        self.display_id = display_id
        self._items_per_page = 100

    @property
    def extended_url(self):
        url = super().extended_url
        if self.display_id is not None:
            url = f"{url}/{self.display_id}"
        return url
