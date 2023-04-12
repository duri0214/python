from unittest import TestCase

from Ddd.domain.models.entities.currency import CurrencyEntity
from Ddd.domain.models.entities.monetary import MonetaryEntity
from Ddd.domain.repositories.monetary import MonetaryRepository


class TestMonetaryRepository(TestCase):
    def setUp(self):
        self.repository = MonetaryRepository()

    def test_add(self):
        monetary1 = MonetaryEntity(100, CurrencyEntity("USD"))
        monetary2 = MonetaryEntity(200, CurrencyEntity("JPY"))

        self.repository.add(monetary1)
        self.repository.add(monetary2)

        self.assertEqual(len(self.repository.data), 2)
        self.assertEqual(self.repository.data[0], monetary1)
        self.assertEqual(self.repository.data[1], monetary2)

    def test_filter_sum(self):
        monetary1 = MonetaryEntity(1000, CurrencyEntity("USD"))
        monetary2 = MonetaryEntity(200, CurrencyEntity("USD"))
        monetary3 = MonetaryEntity(3000, CurrencyEntity("JPY"))

        self.repository.add(monetary1)
        self.repository.add(monetary2)
        self.repository.add(monetary3)

        self.assertEqual(self.repository.filter_sum(CurrencyEntity("USD")), "1,200.0USD")
        self.assertEqual(self.repository.filter_sum(CurrencyEntity("JPY")), "3,000.0JPY")
