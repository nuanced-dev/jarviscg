def func(c):
    for i in c:
        pass


class Cls:
    def __init__(self, max=0):
        self.max = max

    def __iter__(self):
        self.n = 10
        return self

    def __next__(self):
        if self.n > self.max:
            raise StopIteration

        result = 2**self.n
        self.n += 1
        return func


func(Cls(10))
