import json
from abc import ABC, abstractmethod
from typing import Callable

class BasePairDataModel(ABC):
    created_at = "YYYY-MM-DD 00:00:00"
    updated_at = "YYYY-MM-DD 00:00:00"
    @abstractmethod
    def return_value(self):
        pass

class AsIsPairDataModel(BasePairDataModel):
    """
    データ構造クラスにラッピングしてそのまま（as is）返す
    """
    def __init__(self, data_a: int, data_b: int):
        self.data_a = data_a
        self.data_b = data_b

    def return_value(self):
        return self.data_a + self.data_b

class TwicePairDataModel(BasePairDataModel):
    """
    データ構造クラスにラッピングして２倍して返す
    """
    def __init__(self, data_c: int, data_d: int):
        self.data_c = data_c
        self.data_d = data_d

    def return_value(self):
        return (self.data_c * 2) + (self.data_d * 2)

def seeding(json_data: str, callback_func: Callable[[int], BasePairDataModel]):
    datas = json.loads(json_data)
    return_value = []
    for data in datas:
        return_value.append(callback_func(data))

    print([x.return_value() for x in return_value])

if __name__ == "__main__":
    data_list_for_as_is = json.dumps([
        {"data_a": 1, "data_b": 2},
        {"data_a": 10, "data_b": 20},
        {"data_a": 5, "data_b": 10},
        {"data_a": 100, "data_b": 200},
        {"data_a": 7, "data_b": 14},
        {"data_a": 50, "data_b": 60},
        {"data_a": 11, "data_b": 12},
        {"data_a": 25, "data_b": 30},
        {"data_a": 18, "data_b": 36},
        {"data_a": 8, "data_b": 16}
    ])
    data_list_for_twice = json.dumps([
        {"data_c": 1, "data_d": 2},
        {"data_c": 10, "data_d": 20},
        {"data_c": 5, "data_d": 10},
        {"data_c": 100, "data_d": 200},
        {"data_c": 7, "data_d": 14},
        {"data_c": 50, "data_d": 60},
        {"data_c": 11, "data_d": 12},
        {"data_c": 25, "data_d": 30},
        {"data_c": 18, "data_d": 36},
        {"data_c": 8, "data_d": 16}
    ])
    seeding(data_list_for_as_is, lambda data: AsIsPairDataModel(data_a=data["data_a"], data_b=data["data_b"]))
    seeding(data_list_for_twice, lambda data: TwicePairDataModel(data_c=data["data_c"], data_d=data["data_d"]))
