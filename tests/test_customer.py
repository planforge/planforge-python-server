import copy
from unittest.mock import MagicMock, patch

import planforge
from planforge.customer import Customer
from planforge.stores import MemoryStore

planforge.server_key = "apikey"
planforge.api_url = "http://localhost:8000/api"

CUSTOMER_DATA = {
    "features": [{"slug": "test_feature", "enabled": True, "name": "Test Feature"}]
}


def mock_data(id):
    data = copy.deepcopy(CUSTOMER_DATA)
    data["id"] = id
    return data


class TestCustomer:
    def teardown_method(self, method):
        planforge.store.clear()

    @patch("requests.get")
    def test_all_stores_data_and_returns(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = [
            mock_data("cus_0000000"),
            mock_data("cus_0000001"),
        ]
        get_mock.return_value = response_mock
        response = Customer.all()
        get_mock.assert_called_once_with(
            "http://localhost:8000/api/customers",
            params={},
            headers={"Authorization": "Bearer apikey"},
        )
        assert response[0].data == mock_data("cus_0000000")
        assert response[1].data == mock_data("cus_0000001")
        assert planforge.store.get("cus_0000000") == mock_data("cus_0000000")
        assert planforge.store.get("cus_0000001") == mock_data("cus_0000001")

    @patch("requests.get")
    def test_get_stores_data_and_returns(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = [
            mock_data("cus_0000000"),
        ]
        get_mock.return_value = response_mock
        response = Customer.get("cus_0000000")
        get_mock.assert_called_once_with(
            "http://localhost:8000/api/customers/cus_0000000",
            params={},
            headers={"Authorization": "Bearer apikey",},
        )
        assert response.data == [mock_data("cus_0000000")]
        assert planforge.store.get("cus_0000000") == [mock_data("cus_0000000")]

    @patch("requests.get")
    def test_get_returns_stored_data_if_api_unreachable(self, get_mock):
        planforge.store.put("cus_0000000", CUSTOMER_DATA)
        get_mock.side_effect = ConnectionError()
        response = Customer.get("cus_0000000")
        assert response.data == CUSTOMER_DATA

    def test_feature_enabled_returns_true(self):
        customer = Customer(CUSTOMER_DATA)
        assert customer.feature("test_feature").enabled

    def test_feature_enabled_returns_false(self):
        data = copy.deepcopy(CUSTOMER_DATA)
        data["features"][0]["enabled"] = False
        customer = Customer(data)
        assert not customer.feature("test_feature").enabled

    def test_feature_enabled_returns_false_if_features_unset(self):
        customer = Customer({})
        assert not customer.feature("test_feature").enabled

    def test_feature_enabled_returns_false_if_key_unset(self):
        customer = Customer({"features": {}})
        assert not customer.feature("test_feature").enabled
