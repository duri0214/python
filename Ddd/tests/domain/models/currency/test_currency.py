from unittest import TestCase

from Ddd.domain.models.currency.currency import Currency


class TestCurrency(TestCase):
    def test_currency_create_jpy(self):
        currency = Currency('JPY')
        self.assertEqual(currency.code, 'JPY')

    def test_currency_create_usd(self):
        currency = Currency('USD')
        self.assertEqual(currency.code, 'USD')

    def test_currency_equality(self):
        jpy1 = Currency('JPY')
        jpy2 = Currency('JPY')
        usd = Currency('USD')
        self.assertEqual(jpy1, jpy2)
        self.assertNotEqual(jpy1, usd)
        self.assertTrue(jpy1 == "JPY")
        self.assertFalse(jpy1 is None)

    def test_currency_equality_with_other_object(self):
        jpy = Currency('JPY')
        self.assertFalse(jpy == 123)
