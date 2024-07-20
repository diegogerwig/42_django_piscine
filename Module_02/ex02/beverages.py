class HotBeverage:
    docs = 'Just some hot water in a cup.'

    def __init__(self, price=0.30, name='hot beverage'):
        self.price = price
        self.name = name

    def description(self):
        return self.docs

    def __str__(self):
        return f'name : {self.name}\nprice : {self.price}\ndescription : {self.description()}\n'


class Coffee(HotBeverage):
    docs = 'A coffee, to stay awake.'

    def __init__(self, price=0.40, name='coffee'):
        super().__init__(price, name)


class Tea(HotBeverage):
    docs = 'Just some hot water in a cup.'

    def __init__(self, price=0.30, name='tea'):
        super().__init__(price, name)


class Chocolate(HotBeverage):
    docs = 'Chocolate, sweet chocolate...'

    def __init__(self, price=0.50, name='chocolate'):
        super().__init__(price, name)


class Cappuccino(HotBeverage):
    docs = 'Un po’ di Italia nella sua tazza!'

    def __init__(self, price=0.45, name='cappuccino'):
        super().__init__(price, name)


def main():
    instance_list = [HotBeverage(), Coffee(), Tea(), Chocolate(), Cappuccino()]
    for instance in instance_list:
        print(instance)


if __name__ == '__main__':
    main()
