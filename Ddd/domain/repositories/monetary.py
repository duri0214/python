from Ddd.domain.models.entities.currency import CurrencyEntity
from Ddd.domain.models.entities.monetary import MonetaryEntity


class MonetaryRepository:
    def __init__(self):
        self.data: list[MonetaryEntity] = []

    def add(self, monetary: MonetaryEntity):
        self.data.append(monetary)

    def filter_sum(self, currency: CurrencyEntity) -> str:
        total: float = 0.
        for item in self.data:
            if item.currency == currency:
                total += item.amount

        return f'{total:,}{currency.code}'
