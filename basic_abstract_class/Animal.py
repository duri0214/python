import abc


class Animal(object, metaclass=abc.ABCMeta):
    """動物を定義するための基底クラス"""
    @abc.abstractmethod
    def say_hello(self):
        pass
