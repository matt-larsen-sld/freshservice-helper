import logging
from ..api import RequestService
from ..endpoints import GenericPluralEndpoint


logger = logging.getLogger(__name__)


class AssetsEndPoint(GenericPluralEndpoint):
    """Endpoint for working with FreshService Assets"""

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

    def delete(self, identifier, permanently=False):
        """Delete an asset with an option to additionally call the endpoint to permanently delete the item."""
        _method = "DELETE"
        self.display_id = identifier
        _url = f"{self.extended_url}"
        logger.info("Deleting asset with display_id = '%d'", self.display_id)
        response = self.send_request(_url, method=_method)
        if permanently:
            _url = f"{self.extended_url}/delete_forever"
            _method = "PUT"
            logger.info(
                "Permanently deleting asset with display_id = '%d'", self.display_id
            )
            response = self.send_request(_url, method=_method)
        return response

    def restore(self, identifier):
        _method = "PUT"
        _url = f"{self.extended_url}/{identifier}/restore"
        response = self.send_request(_url, method=_method)
        return response
