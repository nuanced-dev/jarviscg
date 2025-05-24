from datetime import datetime
import multiprocessing

class FixtureClass():
    def __init__(self):
        self.current_time = None

    def foo(self) -> None:
        multiprocessing.Pipe()
        self.current_time = datetime.now()

    def bar(self) -> None:
        self.foo()
