from datetime import datetime
import multiprocessing
from multiprocessing import Process

class FixtureClass():
    def __init__(self):
        self.current_time = None

    def foo(self) -> None:
        multiprocessing.Pipe()
        Process()
        self.current_time = datetime.now()

    def bar(self) -> None:
        self.foo()
