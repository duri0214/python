import json
from typing import Self

from Ddd.domain.models.currency.currency import Currency
from Ddd.domain.models.serializable import Serializable


class Monetary(Serializable):
    def __init__(self, amount: int, currency: Currency):
        self.amount: int = amount
        self.currency: Currency = currency

    def to_json(self) -> json:
        temp_dict = {"amount": self.amount, "currency": self.currency.to_dict()}

        return json.dumps(temp_dict)

    @staticmethod
    def from_json(json_str: str) -> Self:
        d = json.loads(json_str)

        return Monetary(d["amount"], d["currency"])

    def __eq__(self, other):
        if isinstance(other, Monetary):
            return self.amount == other.amount and self.currency == other.currency

        return False
