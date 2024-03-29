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

    assert end_point.request_service.session.prepare_request.called_once()
    assert end_point.request_service.session.send.called_once()


@patch.object(GenericEndPoint, "send_request")
def test_create_does_not_send_null_values_in_data_to_send_request(fake_request_service):
    """Given data that has None values, check that create removes the fields with None values before passing the data
    to the send_request method
    """
    with fake_request_service as fake_rs:
        end_point = GenericEndPoint(fake_rs)
        _data = {"a": "a", "b": None}
        _ = end_point.create(_data, True)
        _send_request_call_data = end_point.send_request.call_args.kwargs.get("data")
        assert _send_request_call_data["a"] == "a"
        with pytest.raises(KeyError):
            _ = _send_request_call_data[
                "b"
            ]  # 'b' should have been removed as a key from data dict.


@patch.object(GenericEndPoint, "send_request")
def test_create_does_not_send_null_values_in_data_to_send_request_recursive(
        fake_request_service,
):
    """Given Dict data that has None values in a nested Dict, check that create removes the fields with None values
    before passing the data to the send_request method
    """
    with fake_request_service as fake_rs:
        end_point = GenericEndPoint(fake_rs)
        _data = {"a": "a", "b": None, "c": {"1": 1, "2": None}}
        _ = end_point.create(_data, True)
        _send_request_call_data = end_point.send_request.call_args.kwargs.get("data")
        assert _send_request_call_data["a"] == "a"
        with pytest.raises(KeyError):
            _ = _send_request_call_data[
                "b"
            ]  # 'b' should have been removed as a key from data dict.
        with pytest.raises(KeyError):
            _ = _send_request_call_data["c"]["2"]


@patch.object(GenericEndPoint, "send_request")
def test_create_does_not_send_values_not_in_creation_fields(fake_request_service, ):
    """Given Dict data that has keys that are not in self.creation_fields, and self.creation_fields is not None check
    that create removes the fields that are not in self.creation_fields before passing the data to the send_request
    method.
    """
    with fake_request_service as fake_rs:
        end_point = GenericEndPoint(fake_rs)
        end_point.creation_fields = ["a", "b", ]
        _data = {"a": "a", "b": "b", "c": {"1": 1, "2": 2}}  # `c` is not in `creation_fields` and should not be sent.
        _ = end_point.create(_data, True)
        _send_request_call_data = end_point.send_request.call_args.kwargs.get("data")
        assert _send_request_call_data["a"] == "a"  # the data from the `a` field was sent; tests that `a`, being in
        # `creation_fields` was sent
        with pytest.raises(KeyError):
            _ = _send_request_call_data["c"]  # `c` should have been removed as a key from the data dict.


@patch.object(GenericEndPoint, "send_request")
def test_create_does_not_send_read_only_fields(fake_request_service, ):
    """Given Dict data that has keys that are in `self.read_only_fields`, check that `self.create` removes those read
    only from the data before passing the data to the `self.send_request` method.
    """
    with fake_request_service as fake_rs:
        end_point = GenericEndPoint(fake_rs)
        end_point.read_only_fields = ("c",)
        _data = {"a": "a", "b": "b", "c": 1}  # `c` is a read only field
        _ = end_point.create(_data, True)
        _send_request_call_data = end_point.send_request.call_args.kwargs.get("data")
        assert _send_request_call_data["a"] == "a"  # the data from `a` field was sent;
        with pytest.raises(KeyError):
            _ = _send_request_call_data["c"]  # `c` is a read only field and should have been removed before being sent.
