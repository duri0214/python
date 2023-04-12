import json
from typing import Self

from Ddd.domain.models.entities.currency import CurrencyEntity
from Ddd.domain.models.serializable import Serializable


class MonetaryEntity(Serializable):
    def __init__(self, amount: float, currency: CurrencyEntity):
        self.amount: float = amount
        self.currency: CurrencyEntity = currency

    def to_json(self) -> json:
        temp_dict = {"amount": self.amount, "currency": self.currency.to_dict()}

        return json.dumps(temp_dict)

    @staticmethod
    def from_json(json_str: str) -> Self:
        d = json.loads(json_str)

        return MonetaryEntity(d["amount"], d["currency"])

    # TODO: add()とかmonetary特有の amount x currency のメソッドの追加
    #  https://dev.to/soumyajyotibiswas/chatgpt-domain-driven-design-and-python-using-openai-to-dive-into-software-development-4ogf

    def __eq__(self, other):
        if isinstance(other, MonetaryEntity):
            return self.amount == other.amount and self.currency == other.currency

        return False
