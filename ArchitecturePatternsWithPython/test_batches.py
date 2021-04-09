import unittest
from datetime import date

from model import Batch, OrderLine, Person, Name


class MyTestCase(unittest.TestCase):
    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=date.today())
        line = OrderLine('order-ref', "SMALL-TABLE", 2)
        batch.allocate(line)
        self.assertEqual(18, batch.available_quantity)

    def make_batch_and_line(self, sku, batch_qty, line_qty):
        return (
            Batch('batch-001', sku, batch_qty, eta=date.today()),
            OrderLine('order-123', sku, line_qty)
        )

    def test_can_allocate_if_available_greater_than_required(self):
        large_batch, small_line = self.make_batch_and_line('ELEGANT-LAMP', 20, 2)
        self.assertTrue(large_batch.can_allocate(small_line))

    def test_cannot_allocate_if_available_smaller_than_required(self):
        small_batch, large_line = self.make_batch_and_line('ELEGANT-LAMP', 2, 20)
        self.assertFalse(small_batch.can_allocate(large_line))

    def test_can_allocate_if_available_equal_to_required(self):
        batch, line = self.make_batch_and_line('ELEGANT-LAMP', 2, 2)
        self.assertTrue(batch.can_allocate(line))

    def test_cannot_allocate_if_skus_do_not_match(self):
        """商品コードが違えば割り当てることはできない"""
        batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
        different_sku_line = OrderLine('order-123', 'EXPENSIVE-TOASTER', 10)
        self.assertFalse(batch.can_allocate(different_sku_line))

    def test_can_only_deallocate_allocated_lines(self):
        batch, unallocated_line = self.make_batch_and_line('DECORATIVE-TRINKET', 20, 2)
        batch.deallocate(unallocated_line)
        self.assertEqual(20, batch.available_quantity)

    def test_can_twice_purchase_ng_purchase1(self):
        """オーダー番号がすでにあるなら注文を受け付けない"""
        batch = Batch('batch-001', 'ELEGANT-LAMP', 20, eta=date.today())
        batch.allocate(OrderLine('order-123', 'ELEGANT-LAMP', 2))
        batch.allocate(OrderLine('order-123', 'ELEGANT-LAMP', 2))
        self.assertEqual(18, batch.available_quantity)

    def test_can_twice_allocate_ok_purchase(self):
        """オーダー番号が違えば2連続注文を受け付ける"""
        batch = Batch('batch-001', 'ELEGANT-LAMP', 20, eta=date.today())
        batch.allocate(OrderLine('order-123', 'ELEGANT-LAMP', 2))
        batch.allocate(OrderLine('order-1233', 'ELEGANT-LAMP', 2))
        self.assertEqual(16, batch.available_quantity)

    def test_can_twice_allocate_ng_purchase2(self):
        """オーダー番号が違っても商品が違うと受け付けない"""
        batch = Batch('batch-001', 'ELEGANT-LAMP', 20, eta=date.today())
        batch.allocate(OrderLine('order-123', 'ELEGANT-LAMP', 2))
        batch.allocate(OrderLine('order-1233', 'ELEGANT-LAMPP', 2))
        self.assertEqual(18, batch.available_quantity)

    def test_barry_is_harry(self):
        harry = Person(Name("Harry", "Percival"))
        barry = harry
        barry.name = Name("Barry", "Percival")
        self.assertTrue(harry is barry and barry is harry)


if __name__ == '__main__':
    unittest.main()
