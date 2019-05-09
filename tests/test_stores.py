from planforge.stores import MemoryStore

class TestMemoryStore:
    def test_get_returns_data_if_present(self):
        store = MemoryStore()
        store._data['hello'] = 'world'
        assert store.get('hello') == 'world'

    def test_get_returns_none_if_not_present(self):
        store = MemoryStore()
        assert store.get('hello') == None

    def test_put_sets_value_and_returns_value(self):
        store = MemoryStore()
        value = store.put('hello', 'world')
        assert value == 'world'
        assert store._data['hello'] == 'world'

    def test_delete_removes_value_and_returns_true(self):
        store = MemoryStore()
        store._data['hello'] = 'world'
        value = store.delete('hello')
        assert value == True
        assert store._data.get('hello') == None

    def test_clear_removes_all_values_and_returns_true(self):
        store = MemoryStore()
        store._data['hello'] = 'world'
        value = store.clear()
        assert value == True
        assert store._data.get('hello') == None
