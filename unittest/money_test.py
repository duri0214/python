import unittest
import abc


class Money(object):
    def __init__(self, amount: int):
        self.amount = amount

    def equals(self, obj) -> bool:
        return self.amount == obj.amount and type(self) == type(obj)

    @abc.abstractmethod
    def times(self, multiplier: int):
        return NotImplementedError

    @classmethod
    def dollar(cls, amount: int):
        return Dollar(amount)

    @classmethod
    def franc(cls, amount: int):
        return Franc(amount)


class Dollar(Money):
    def times(self, multiplier: int):
        return Dollar(self.amount * multiplier)


class Franc(Money):
    def times(self, multiplier: int):
        return Franc(self.amount * multiplier)


class TestMoney(unittest.TestCase):

    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10).amount, five.times(2).amount)
        self.assertEqual(Money.dollar(15).amount, five.times(3).amount)

    def test_equality(self):
        self.assertTrue(Money.dollar(5).equals(Money.dollar(5)))
        self.assertFalse(Money.dollar(5).equals(Money.dollar(6)))
        self.assertTrue(Money.franc(5).equals(Money.franc(5)))
        self.assertFalse(Money.franc(5).equals(Money.franc(6)))
        self.assertFalse(Money.franc(5).equals(Money.dollar(5)))

    def testFrancMultiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10).amount, five.times(2).amount)
        self.assertEqual(Money.franc(15).amount, five.times(3).amount)


if __name__ == '__main__':
    unittest.main()
