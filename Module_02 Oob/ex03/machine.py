import random
from beverages import Cappuccino, Chocolate, Coffee, HotBeverage, Tea


class CoffeeMachine:
    def __init__(self) -> None:
        self.count = 0

    class EmptyCup(HotBeverage):

        def __init__(self, price=0.90, name='empty cup') -> None:
            super().__init__(price, name)

        def description(self) -> str:
            return 'An empty cup?! Gimme my money back!'

    class BrokenMachineException(Exception): # The Exception class is a built-in class in Python that defines the base class for all built-in exceptions.

        def __init__(self, message='❗ This coffee machine has to be repaired.') -> None:
            super().__init__(message)

    def repair(self) -> None:
        self.count = 0
        print('✅ This coffee machine has been repaired\n')

    def serve(self, beverage) -> HotBeverage:
        self.count += 1
        if self.count > 10:
            raise self.BrokenMachineException()
        
        if random.randrange(2) == 0:
            return beverage()
        else:
            return self.EmptyCup()


def test():
    beverages_dict = {0: HotBeverage, 1: Coffee, 2: Tea, 3: Chocolate, 4: Cappuccino}
    iterations = 25
        
    machine = CoffeeMachine()
    for i in range(iterations):
        print(f'Iteration {i + 1} from {iterations}')
        try:
            print(machine.serve(beverages_dict.get(random.randrange(5))))
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            machine.repair()


if __name__ == '__main__':
    test()
