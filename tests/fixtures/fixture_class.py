from datetime import datetime
from functools import cache
from multiprocessing import Process

class FixtureClass():
    def __init__(self):
        self.current_time = None

    def foo(self) -> None:
        cache(self.foo)
        Process()
        self.current_time = datetime.now()

    def bar(self) -> None:
        self.foo()
