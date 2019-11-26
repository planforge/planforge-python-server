from unittest.mock import MagicMock, patch

import pytest

import planforge
from planforge.errors import PlanForgeApiException
from planforge.api_requestor import ApiRequestor

planforge.server_key = "apikey"
planforge.api_base = "http://localhost:8000/api"


class TestApiRequestor:
    @patch("requests.get")
    def test_get_sets_proper_params(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        get_mock.return_value = response_mock

        api_requestor = ApiRequestor().get("/test")
        get_mock.assert_called_once_with(
            "http://localhost:8000/api/test",
            params={},
            headers={"Authorization": "Bearer apikey"},
        )

    @patch("requests.get")
    def test_get_throws_exception_for_non_200_response(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 403
        response_mock.json.return_value = {"error": "Server Error"}
        get_mock.return_value = response_mock

        with pytest.raises(PlanForgeApiException):
            api_requestor = ApiRequestor().get("/test")

    @patch("requests.get")
    def test_get_returns_json(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {"hello": "world"}
        get_mock.return_value = response_mock

        response = ApiRequestor().get("/test")
        response_mock.json.assert_called_once_with()
        assert response == {"hello": "world"}
