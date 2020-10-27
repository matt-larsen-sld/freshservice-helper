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
        self.resource_key = None
        self.create_command = None

    def get(self):
        raise NotImplemented

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

    def create(self, data: dict) -> dict:
        url = self.extended_url
        if self.create_command is not None:
            url = f"{url}/{self.create_command}"
        if self.fs_create_requests_enabled:
            try:
                response = self.send_request(url, method="POST", data=data)
            except HTTPError as err:
                logger.error("Error encountered with send_request %s", err)
                logger.warning(
                    "send_request called to url '%s' method 'POST' and data %s",
                    url,
                    err.request.body,
                )
                logger.warning(
                    "Response: 'status_code' == '%d', 'text' == '%s'",
                    err.response.status_code,
                    err.response.text,
                )
                raise err
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

    def send_request(self, url, method="GET", data=None):
        if isinstance(data, dict):
            data = json.dumps(data)
        req = Request(method, url, headers=self.DEFAULT_HEADERS, data=data)
        prepped_req = self.request_service.session.prepare_request(req)
        resp = self.request_service.session.send(prepped_req)
        resp.raise_for_status()
        return resp.json()


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
        pagination_part = f"page={page}&per_page={self.items_per_page}"
        if query:
            url = f"{self.extended_url}?{pagination_part}&{query}"
        else:
            url = f"{self.extended_url}?{pagination_part}"
        return url
