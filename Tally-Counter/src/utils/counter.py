class Counter:
    def __init__(self, count, increment_value, decrement_value, symbol):
        self.count = count
        self.increment_value = increment_value
        self.decrement_value = decrement_value
        self.symbol = symbol

    def increment(self):
        self.count += self.increment_value

    def decrement(self):
        self.count -= self.decrement_value

    def reset(self):
        self.count = 0