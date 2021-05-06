from unittest.mock import MagicMock

import pytest

from fshelper import Credential, RequestService


@pytest.fixture(scope="function")
def fake_credential(faker):
    username = faker.hexify(text="^^^^^^^^^^^^^")
    password = faker.hexify(text="^^^^^^^^^^^^^")
    credential = Credential(username, password)
    return credential


@pytest.fixture(scope="function")
def fake_fs_domain(faker):
    return faker.hexify(text="^^^^^^^^^^^")


@pytest.fixture(scope="function")
def fake_request_service(faker):
    mock_request_service = MagicMock(RequestService)
    mock_request_service.domain = faker.hexify(text="^^^^^^^^^^")
    return mock_request_service
