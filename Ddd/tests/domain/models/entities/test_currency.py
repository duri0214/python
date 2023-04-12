from unittest import TestCase

from Ddd.domain.models.entities.currency import CurrencyEntity


class TestCurrency(TestCase):
    def test_currency_create_jpy(self):
        currency = CurrencyEntity('JPY')
        self.assertEqual(currency.code, 'JPY')

    def test_currency_create_usd(self):
        currency = CurrencyEntity('USD')
        self.assertEqual(currency.code, 'USD')

    def test_currency_equality(self):
        jpy1 = CurrencyEntity('JPY')
        jpy2 = CurrencyEntity('JPY')
        usd = CurrencyEntity('USD')
        self.assertEqual(jpy1, jpy2)
        self.assertNotEqual(jpy1, usd)
        self.assertTrue(jpy1 == "JPY")
        self.assertFalse(jpy1 is None)

    def test_currency_equality_with_other_object(self):
        jpy = CurrencyEntity('JPY')
        self.assertFalse(jpy == 123)
