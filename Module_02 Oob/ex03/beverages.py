class HotBeverage:

    def __init__(self, price=0.30, name='hot beverage') -> None:
        self.price = price
        self.name = name
    
    def description(self) -> str:
        return 'Just some hot water in a cup.'

    def __str__(self) -> str:
        return f'name : {self.name}\nprice : {self.price:.2f}\ndescription : {self.description()}\n'


class Coffee(HotBeverage):

    def __init__(self, price=0.40, name='coffee') -> None:
        super().__init__(price, name)

    def description(self) -> str:
        return 'A coffee, to stay awake.'


class Tea(HotBeverage):

    def __init__(self, price=0.30, name='tea') -> None:
        super().__init__(price, name)

    def description(self) -> str:
        return 'Just some hot water in a cup.'


class Chocolate(HotBeverage):

    def __init__(self, price=0.50, name='chocolate') -> None:
        super().__init__(price, name)

    def description(self) -> str:
        return 'Chocolate, sweet chocolate...'


class Cappuccino(HotBeverage):

    def __init__(self, price=0.45, name='cappuccino') -> None:
        super().__init__(price, name)

    def description(self) -> str:
        return 'Un po’ di Italia nella sua tazza!'


def test():
    instance_list = [HotBeverage(), Coffee(), Tea(), Chocolate(), Cappuccino()]
    for instance in instance_list:
        print(instance)


if __name__ == '__main__':
    test()
