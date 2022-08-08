from unittest.mock import MagicMock, patch

import pytest

from fshelper import RequestService
from fshelper.v2 import AssetsEndPoint


class AssetTests:
    @pytest.fixture
    def mock_request_service(self, faker):
        mock_request_service = MagicMock(RequestService)
        mock_request_service = faker.hexify(text="^^^^^^^^")
        return mock_request_service

