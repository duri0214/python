from basic_abstract_class.Animal import Animal


class Dog(Animal):
    """犬を定義"""
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        return "こんにちは！私の名前は" + self.name + "だワン！"


class Cat(Animal):
    """猫を定義"""
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        return "こんにちは！私の名前は" + self.name + "だネコ！"


d = Dog("ポチ")
c = Cat("きゅうべぇ")
print(d.say_hello(), c.say_hello())
