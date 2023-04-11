from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(json_str: str):
        pass
