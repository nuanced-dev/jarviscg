class A:
    def __init__(self):
        def f():
            pass

        f()
        pass


class B(A):
    def __init__(self):
        super().__init__()


class C(B):
    def __init__(self):
        super().__init__()


c = C()
