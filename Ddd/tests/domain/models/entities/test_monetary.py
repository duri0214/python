import unittest

from Ddd.domain.models.entities.currency import CurrencyEntity
from Ddd.domain.models.entities.monetary import MonetaryEntity


class MonetaryTest(unittest.TestCase):
    def test_to_json(self):
        jpy = CurrencyEntity("JPY")
        monetary = MonetaryEntity(1000, jpy)

        expected_json = '{"amount": 1000, "currency": {"code": "JPY"}}'
        self.assertEqual(monetary.to_json(), expected_json)

    def test_from_json(self):
        json_data = '{"amount": 2000, "currency": "USD"}'
        deserialized_monetary = MonetaryEntity.from_json(json_data)

        self.assertIsInstance(deserialized_monetary, MonetaryEntity)
        self.assertEqual(deserialized_monetary.amount, 2000)
        self.assertEqual(deserialized_monetary.currency, "USD")
