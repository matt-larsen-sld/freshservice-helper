from unittest.mock import MagicMock, patch

import pytest
from requests import Session

from fshelper import RequestService
from fshelper.endpoints import GenericEndPoint, GenericPluralEndpoint

# https://faker.readthedocs.io/en/master/pytest-fixtures.html


@pytest.fixture
def mock_request_service(faker):
    mock_request_service = MagicMock(RequestService)
    mock_request_service.domain = faker.hexify(text="^^^^^^^^^^")
    return mock_request_service


def test_generic_end_point_base_url(mock_request_service):
    generic_endpoint = GenericEndPoint(mock_request_service)
    assert mock_request_service.domain in generic_endpoint.base_url


def test_generic_plural_end_point_base_url(mock_request_service):
    plural_endpoint = GenericPluralEndpoint(mock_request_service)
    assert mock_request_service.domain in plural_endpoint.base_url


def test_generic_plural_end_point_get_url(mock_request_service):
    plural_endpoint = GenericPluralEndpoint(mock_request_service)
    assert mock_request_service.domain in plural_endpoint.paginate_url()


def test_generic_plural_end_point_get_url_page_num(faker, mock_request_service):
    plural_endpoint = GenericPluralEndpoint(mock_request_service)
    page_number = faker.pyint()
    assert str(page_number) in plural_endpoint.paginate_url(page=page_number)


def test_generic_plural_end_point_get_url_query(faker, mock_request_service):
    plural_endpoint = GenericPluralEndpoint(mock_request_service)
    query = "some_id=123"
    assert query in plural_endpoint.paginate_url(query)


@patch("fshelper.api.Session", spec=Session)
def test_generic_plural_end_point_send_request_session_session_methods_called(
        _, fake_credential, fake_fs_domain
):
    patched_request_service = RequestService(fake_credential, fake_fs_domain)
    with patched_request_service as request_service:
        plural_endpoint = GenericPluralEndpoint(request_service)
        url = plural_endpoint.paginate_url()
        _ = plural_endpoint.send_request(url)
    assert plural_endpoint.request_service.session.prepare_request.called is True
    assert plural_endpoint.request_service.session.send.called is True
    assert (
            plural_endpoint.request_service.session.send.return_value.raise_for_status.called
            is True
    )


def test_generic_end_point_get_method_calls_send_request(fake_request_service, faker):
    _id = faker.pyint()
    with fake_request_service as fake_service:
        end_point = GenericEndPoint(fake_service)
        _ = end_point.get(_id)
    assert end_point.request_service.session.prepare_request.called_once()
    assert end_point.request_service.session.send.called_once()

