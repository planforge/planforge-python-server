import json
import os

from requests.exceptions import ConnectionError

import planforge
from planforge.api_requestor import ApiRequestor


class PlanForgeObject(dict):
    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        del self[k]


class Customer(PlanForgeObject):
    @classmethod
    def retrieve(cls, id):
        from planforge import store

        key = f"customer:{id}"
        data = json.loads(store.get(key))
        return cls(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["subscriptions"] = self._build_subscriptions()
        self["features"] = self._build_features()

    def _build_subscriptions(self):
        subscriptions = self.get("subscriptions", [])
        ret = []
        for subscription in subscriptions:
            if isinstance(subscription, CustomerSubscription):
                ret.append(subscription)
            else:
                ret.append(CustomerSubscription(subscription))
        return ret

    def _build_features(self):
        features = self.get("features", [])
        ret = []
        for feature in features:
            if isinstance(feature, CustomerFeature):
                ret.append(feature)
            else:
                cf = CustomerFeature(feature)
                if cf.get("subscription") is not None:
                    cf["subscription"] = self.subscription(cf["subscription"])
                ret.append(cf)
        return ret

    def feature(self, key):
        features = self.get("features", [])
        for feature in features:
            if feature["slug"] == key:
                return feature
        return CustomerFeature()

    def subscription(self, key):
        subscriptions = self.get("subscriptions", [])
        for subscription in subscriptions:
            if subscription["id"] == key:
                return CustomerSubscription(subscription)
        return None


class CustomerFeature(PlanForgeObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.get("enabled") is None:
            self["enabled"] = False


class CustomerSubscription(PlanForgeObject):
    pass
