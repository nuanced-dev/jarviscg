class A:
    def __init__(self):
        pass


class B:
    def __init__(self) -> None:
        pass

    def func(self):
        pass


class C(A, B):
    def __init__(self):
        pass

    def func(self):
        pass


c = C()
c.func()
