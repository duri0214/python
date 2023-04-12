from typing import Self


class CurrencyEntity:
    def __init__(self, code: str):
        self._code = code

    @property
    def code(self):
        return self._code

    def __eq__(self, other: Self | str) -> bool:
        if isinstance(other, CurrencyEntity):
            return self.code == other.code
        elif isinstance(other, str):
            return self.code == other
        else:
            return False

    def to_dict(self) -> dict:
        return {"code": self.code}
