from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from faker import Faker
from requests import Session

from fshelper import RequestService, ServiceItemsEndPoint
from .factories import FreshServiceServiceItemsResponseProvider

faker = Faker()
faker.add_provider(FreshServiceServiceItemsResponseProvider)


@pytest.fixture
def mock_request_service():
    mock_request_service = MagicMock(RequestService)
    mock_request_service.domain = faker.hexify(text="^^^^^^^^^^")
    return mock_request_service


def test_service_items_base_url(mock_request_service):
    service_items = ServiceItemsEndPoint(mock_request_service)
    assert mock_request_service.domain in service_items.base_url


def test_service_items_extended_url(mock_request_service):
    service_items = ServiceItemsEndPoint(mock_request_service)
    assert mock_request_service.domain in service_items.extended_url


@patch("fshelper.api.Session", spec=Session)
def test_service_items_end_point_get_all_yields_generator(
    _, fake_credential, fake_fs_domain
):
    patched_request_service = RequestService(fake_credential, fake_fs_domain)
    with patched_request_service as request_service:
        service_items_endpoint = ServiceItemsEndPoint(request_service)
        service_items_generator = service_items_endpoint.get_all()
    assert isinstance(service_items_generator, Generator)


@patch("fshelper.api.Session", spec=Session)
def test_service_items_end_point_get_all_response_count_nb_items_less_than_items_per_page(
    _,
    fake_credential,
    fake_fs_domain,
):
    nb_service_items = None

    def fake_send_request(_):
        return faker.service_items_response(nb_service_items)

    patched_request_service = RequestService(fake_credential, fake_fs_domain)
    with patched_request_service as request_service:
        service_items_endpoint = ServiceItemsEndPoint(request_service)
        service_items_endpoint.send_request = fake_send_request
        nb_service_items = service_items_endpoint.items_per_page - 1
        items = []
        for response in service_items_endpoint.get_all():
            items.extend(response)
    assert len(items) == nb_service_items


@patch("fshelper.api.Session", spec=Session)
def test_service_items_end_point_get_all_response_count_nb_items_greater_than_items_per_page(
    _,
    fake_credential,
    fake_fs_domain,
):
    nb_service_items = None
    nb_pages = 3
    final_nb_items = 10

    def page_countdown(_):
        nonlocal nb_pages
        nonlocal nb_service_items
        nonlocal final_nb_items
        nb_pages -= 1
        if nb_pages == 0:
            nb_service_items = final_nb_items

    def fake_send_request(_):
        resp = faker.service_items_response(nb_service_items)
        page_countdown(None)
        return resp

    patched_request_service = RequestService(fake_credential, fake_fs_domain)
    with patched_request_service as request_service:
        service_items_endpoint = ServiceItemsEndPoint(request_service)
        service_items_endpoint.send_request = fake_send_request
        expected_nb_results = (
            service_items_endpoint.items_per_page * nb_pages + final_nb_items
        )
        while nb_pages > 0:
            nb_service_items = service_items_endpoint.items_per_page
            items = []
            for response in service_items_endpoint.get_all():
                items.extend(response)
    assert len(items) == expected_nb_results


def test_service_items_extended_url_with_display_id(mock_request_service):
    display_id = faker.pyint()
    service_items_end_point = ServiceItemsEndPoint(
        mock_request_service, display_id=display_id
    )
    assert str(display_id) in service_items_end_point.extended_url


def test_service_items_create_called_with_create_command_in_url(
    mock_request_service, monkeypatch
):
    display_id = faker.pyint()
    monkeypatch.setenv("ALLOW_FS_CREATE_REQUESTS", "True")
    with mock_request_service as fake_request_service:
        service_items_end_point = ServiceItemsEndPoint(
            fake_request_service, display_id=display_id
        )
        service_items_end_point.send_request = MagicMock()
        service_items_end_point.send_request.return_value = {"foo": "bar"}
        _ = service_items_end_point.create({"blah": "blah"})
        call_args = [arg for arg in service_items_end_point.send_request.call_args]
        assert service_items_end_point.create_command in str(call_args)


def test_service_items_send_request_not_called_when_env_var_not_set(
    mock_request_service, monkeypatch
):
    display_id = faker.pyint()
    with mock_request_service as fake_request_service:
        service_items_end_point = ServiceItemsEndPoint(
            fake_request_service, display_id=display_id
        )
        service_items_end_point.send_request = MagicMock()
        service_items_end_point.send_request.return_value = {"foo": "bar"}
        _ = service_items_end_point.create({"blah": "blah"})
        assert service_items_end_point.send_request.called is False
