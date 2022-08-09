import re
import pytest
from unittest.mock import MagicMock, patch
from requests import Request

from fshelper import RequestService
from fshelper.v2 import AssetsEndPoint


class TestAssets:
    @pytest.fixture
    def mock_request_service(self, faker):
        mock_request_service = MagicMock(RequestService)
        mock_request_service.domain = faker.hexify(text="^^^^^^^^")
        return mock_request_service

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_get_called_with_id_as_arg_to_constructor(
        self, mock_request, mock_request_service, faker
    ):
        """get() method has the ID given to the AssetsEndPoint constructor, and then it's used in the URL argument given
        to the Request object.
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service, _id)
            _ = end_point.get()
        args, _ = mock_request.call_args
        assert "GET" in args
        assert any(arg for arg in args if re.search(f".*/{_id}\??", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_delete_called_with_delete_given_to_request_object(
        self, mock_request, mock_request_service, faker
    ):
        """DELETE should be an argument when creating the Request object."""
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.delete(_id)
        args, _ = mock_request.call_args
        assert "DELETE" in args

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_delete_called_with_id_in_request_object_url(
        self, mock_request, mock_request_service, faker
    ):
        """The id should be in one of the arguments to create the Request object."""
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.delete(_id)
        args, _ = mock_request.call_args
        assert any([arg for arg in args if str(_id) in arg])

    def test_delete_calls_send_twice(self, mock_request_service, faker):
        """Calling delete with permanently == True should call send twice.  Once for the delete call with the DELETE
        method, the second a PUT call.
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.delete(_id, permanently=True)
        assert end_point.request_service.session.send.call_count == 2

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_delete_permanently_sends_put_request_last(
        self, mock_request, mock_request_service, faker
    ):
        """Calling delete with permanently == True should call send twice.  First for the delete call with the DELETE
        method, the second a PUT call.
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.delete(_id, permanently=True)
        args, _ = mock_request.call_args
        assert "PUT" in args

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_requests_in_url_for_get_associated_requests(
        self, mock_request, mock_request_service, faker
    ):
        """Calling get_associated_requests should have an argument to the Request object with 'requests'
        at the end of url argument. https://api.freshservice.com/#list_all_asset_requests
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service, _id)
            _ = end_point.get_associated_requests()
        args, _ = mock_request.call_args
        assert any(arg for arg in args if re.search(f".*/{_id}/requests\??", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_requests_in_url_for_get_associated_request_with_id_given_to_method(
        self, mock_request, mock_request_service, faker
    ):
        """Calling get_associated_requests should have an argument to the Request object with 'requests'
        at the end of url argument. This test passed the identifier to the method instead of the constructor.
        https://api.freshservice.com/#list_all_asset_requests
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.get_associated_requests(_id)
        args, _ = mock_request.call_args
        assert any(arg for arg in args if re.search(f".*/{_id}/requests\??", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_restore_in_url_for_request_args(
        self, mock_request, mock_request_service, faker
    ):
        """Calling restore() should have an argument to the Request object with 'restore' at the end of the url
        argument.
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service, _id)
            _ = end_point.restore()
        args, _ = mock_request.call_args
        assert any(arg for arg in args if re.search(f".*/{_id}/restore$", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_restore_in_url_for_request_args_with_id_passed_to_restore_method(
        self, mock_request, mock_request_service, faker
    ):
        """Calling restore() should have an argument to the Request object with 'restore' at the end of the url
        argument.  Passing the ID to the restore method in this test.
        """
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.restore(_id)
        args, _ = mock_request.call_args
        assert any(arg for arg in args if re.search(f".*/{_id}/restore$", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_update_called_with_put_id_request_constructor(
        self, mock_request, mock_request_service, faker
    ):
        """Calling update() should create a PUT request with the ID at the end of the URL."""
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service, _id)
            _ = end_point.update(
                {"foo": "bar"},
            )
        args, _ = mock_request.call_args
        assert "PUT" in args
        assert any(arg for arg in args if re.search(f".*/{_id}$", arg))

    @patch("fshelper.endpoints.Request", spec=Request)
    def test_update_called_with_put_id_in_update_method(
        self, mock_request, mock_request_service, faker
    ):
        """Calling update() should create a PUT request with the ID at the end of the URL."""
        _id = faker.pyint()
        with mock_request_service as mock_service:
            end_point = AssetsEndPoint(mock_service)
            _ = end_point.update({"foo": "bar"}, _id)
        args, _ = mock_request.call_args
        assert "PUT" in args
        assert any(arg for arg in args if re.search(f".*/{_id}$", arg))
