from dataclasses import dataclass
from datetime import date
from typing import Optional, List


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class OutOfStock(Exception):
    pass


class Batch:
    """SKU：Stock Keeping Unit"""
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        """sku（最小管理単位）が同じで、skuの在庫がline.qty以上あれば true"""
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __str__(self):
        return self.sku


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Person:
    def __init__(self, name: Name):
        self.name = name


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    """batchesをソートした上で先頭の要素にallocateを実行"""
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
