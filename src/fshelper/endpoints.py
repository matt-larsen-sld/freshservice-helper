import json
import logging
import os
import sys

from requests import Request
from requests.exceptions import HTTPError

from .api import RequestService

logger = logging.getLogger(__name__)


class GenericEndPoint:
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(self, request_service: RequestService):
        self.request_service = request_service
        self._endpoint = ""
        self.resource_key = None  # dictionary key in the API response data for a resource. Used to access item.
        self.create_command = None  # Some resources extend the endpoint URL with a verb when creating the resource

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def base_url(self):
        return f"https://{self.request_service.domain}.freshservice.com"

    @property
    def extended_url(self):
        return f"{self.base_url}{self.endpoint}"

    @property
    def fs_create_requests_enabled(self):
        return (
            True
            if os.getenv("ALLOW_FS_CREATE_REQUESTS", "False").lower() == "true"
            else False
        )

    def get(self, identifier):
        """Get a single resource from the FS API

        TODO: Check if identifier is already in the extended_url
        """
        _url = f"{self.extended_url}/{identifier}"
        response = self.send_request(_url)
        return response

    def create(self, data: dict) -> dict:
        url = self.extended_url
        if self.create_command is not None:
            url = f"{url}/{self.create_command}"
        if self.fs_create_requests_enabled:
            response = self.send_request(url, method="POST", data=data)
        else:
            logger.warning(
                "Environment variable 'ALLOW_FS_CREATE_REQUESTS' must be set to 'True' to allow sending "
                "FreshService create requests."
            )
            logger.info(
                "Would have sent 'POST' request to '%s' with data '%s'",
                url,
                json.dumps(data),
            )
            response = {"service_request": {"id": sys.maxsize}}
        return response

    def delete(self, identifier):
        """Delete a resource with the FS API

        TODO: Check if the identifier is already in the extended_url
        """
        _method = "DELETE"
        _url = f"{self.extended_url}/{identifier}"
        response = self.send_request(_url, method=_method)
        return response

    def send_request(self, url, method="GET", data=None):
        """Send the HTTP request to the FreshService API using a requests library session.

        TODO: Send query strings as a dict for parameters to the requests API.
        """
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            logger.debug("Generating '%s' request for '%s'", method, url)
            req = Request(method, url, headers=self.DEFAULT_HEADERS, data=data)
            prepped_req = self.request_service.session.prepare_request(req)
            resp = self.request_service.session.send(prepped_req)
            resp.raise_for_status()
            return resp.json()
        except HTTPError as err:
            logger.error("Error encounter with send_request %s", err)
            logger.warning(
                "send_request called to url '%s' with method '%s' and data '%s'",
                url,
                method,
                err.request.body,
            )
            logger.warning(
                "Response: 'status_code' == '%d', 'text' == '%s'",
                err.response.status_code,
                err.response.text,
            )
            raise err


class GenericPluralEndpoint(GenericEndPoint):
    DEFAULT_ITEMS_PER_PAGE = 30

    def __init__(self, request_service: RequestService):
        super(GenericPluralEndpoint, self).__init__(request_service)
        self._items_per_page = None

    @property
    def items_per_page(self):
        return (
            self._items_per_page
            if self._items_per_page
            else self.DEFAULT_ITEMS_PER_PAGE
        )

    def get_all(self, query=None):
        """Sends a paginated get request for items of the resource type identified by self.resource_key.
        From the list of dict in the response yields the items selected by self.resource_key.

        Yields a list of dict items from the response selected by self.resource_key until all page results are returned
        in the request.
        TODO: an argument to automatically add "include=type_fields" to the query rather than have the user specifically
            include that.
        """
        page = 1
        url = self.paginate_url(query, page)
        more_results = True
        while more_results:
            result = self.send_request(url)
            items = result.get(self.resource_key)
            if len(items) < self.items_per_page:
                more_results = False
                yield items
            else:
                page += 1
                url = self.paginate_url(query, page)
                yield items

    def paginate_url(self, query=None, page=1):
        """Add page and per_page paramters to the query string.

        TODO: Change this to manipulate a dict and handle pagination with the send_request method and that dict.
        """
        pagination_part = f"page={page}&per_page={self.items_per_page}"
        if query:
            url = f"{self.extended_url}?{pagination_part}&{query}"
        else:
            url = f"{self.extended_url}?{pagination_part}"
        return url
