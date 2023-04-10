from typing import Self


class Currency:
    def __init__(self, code: str):
        self.code = code

    def __eq__(self, other: Self | str) -> bool:
        if isinstance(other, Currency):
            return self.code == other.code
        elif isinstance(other, str):
            return self.code == other
        else:
            return False
