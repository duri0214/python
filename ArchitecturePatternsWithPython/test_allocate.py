import unittest
import datetime

import pytest

from model import Batch, OrderLine, allocate, OutOfStock


class MyTestCase(unittest.TestCase):
    def test_prefers_current_stock_batches_to_shipments(self=None):
        """batchesの最初のひとつめにしか処理がかからないことを確認"""
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1))
        in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
        shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=tomorrow)
        line = OrderLine('oref', 'RETRO-CLOCK', 10)
        allocate(line, [in_stock_batch, shipment_batch])
        self.assertEqual(90, in_stock_batch.available_quantity)
        self.assertEqual(100, shipment_batch.available_quantity)

    def test_prefers_earlier_batches(self):
        """batchesをソートした上で先頭の要素にallocateが実行されることを確認"""
        today = datetime.datetime.now()
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1))
        later = (datetime.datetime.now() + datetime.timedelta(weeks=4))
        earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today)
        medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow)
        latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=later)
        line = OrderLine('order1', 'MINIMALIST-SPOON', 10)
        allocate(line, [medium, earliest, latest])  # 順番に注目earliestは2番目
        self.assertEqual(90, earliest.available_quantity)  # 2番目にあるearliestにオーダーがかかった
        self.assertEqual(100, medium.available_quantity)
        self.assertEqual(100, latest.available_quantity)

    def test_returns_allocated_batch_ref(self):
        """Batchとallocateの返却が一致することを確認"""
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1))
        in_stock_batch = Batch('in-stock-batch-ref', 'HIGHBROW-POSTER', 100, eta=None)
        shipment_batch = Batch('shipment-batch-ref', 'HIGHBROW-POSTER', 100, eta=tomorrow)
        line = OrderLine('oref', 'HIGHBROW-POSTER', 10)
        allocation = allocate(line, [in_stock_batch, shipment_batch])
        self.assertTrue(allocation == in_stock_batch.reference)

    def test_raises_out_of_stock_exception_if_cannot_allocate(self):
        batch = Batch('batch1', 'SMALL-FORK', 10, eta=datetime.datetime.now())
        line = OrderLine('order1', 'SMALL-FORK', 10)
        allocate(line, [batch])
        with pytest.raises(OutOfStock, match='SMALL-FORK'):
            line = OrderLine('order2', 'SMALL-FORK', 1)
            allocate(line, [batch])


if __name__ == '__main__':
    unittest.main()
