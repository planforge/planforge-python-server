import copy
from unittest.mock import MagicMock, patch

import planforge
from planforge.customer import Customer
from planforge.stores import MemoryStore

planforge.api_key = 'apikey'

CUSTOMER_DATA = {
    'features': {
        'test_feature': {
            'slug': 'test_feature',
            'enabled': True,
            'name': 'Test Feature'
        }
    }
}

class TestCustomer:
    def teardown_method(self, method):
        planforge.store.clear()

    @patch('requests.get')
    def test_all_stores_data_and_returns(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            'cus_0000000': CUSTOMER_DATA,
            'cus_0000001': CUSTOMER_DATA
        }
        get_mock.return_value = response_mock
        response = Customer.all()
        get_mock.assert_called_once_with(
            'http://localhost:8000/api/state',
            params={},
            headers={
                'Authorization': 'Bearer apikey'
            }
        )
        assert response[0].data == CUSTOMER_DATA
        assert response[1].data == CUSTOMER_DATA
        assert planforge.store.get('cus_0000000') == CUSTOMER_DATA
        assert planforge.store.get('cus_0000001') == CUSTOMER_DATA

    @patch('requests.get')
    def test_get_stores_data_and_returns(self, get_mock):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            'cus_0000000': CUSTOMER_DATA,
        }
        get_mock.return_value = response_mock
        response = Customer.get('cus_0000000')
        get_mock.assert_called_once_with(
            'http://localhost:8000/api/state',
            params={
                'customer': 'cus_0000000',
            },
            headers={
                'Authorization': 'Bearer apikey',
            }
        )
        assert response.data == CUSTOMER_DATA
        assert planforge.store.get('cus_0000000') == CUSTOMER_DATA

    @patch('requests.get')
    def test_get_returns_stored_data_if_api_unreachable(self, get_mock):
        planforge.store.put('cus_0000000', CUSTOMER_DATA)
        get_mock.side_effect = ConnectionError()
        response = Customer.get('cus_0000000')
        assert response.data == CUSTOMER_DATA

    def test_feature_enabled_returns_true(self):
        customer = Customer(CUSTOMER_DATA)
        assert customer.feature_enabled('test_feature')

    def test_feature_enabled_returns_false(self):
        data = copy.deepcopy(CUSTOMER_DATA)
        data['features']['test_feature']['enabled'] = False
        customer = Customer(data)
        assert not customer.feature_enabled('test_feature')

    def test_feature_enabled_returns_false_if_features_unset(self):
        customer = Customer({})
        assert not customer.feature_enabled('test_feature')

    def test_feature_enabled_returns_false_if_key_unset(self):
        customer = Customer({'features': {}})
        assert not customer.feature_enabled('test_feature')
