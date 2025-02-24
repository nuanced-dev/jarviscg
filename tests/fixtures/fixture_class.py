from datetime import datetime
from fixtures._utils.util import util_function

def invoke_util_function() -> None:
    util_function()

class FixtureClass():
    def __init__(self):
        self.tzinfo = None

    def foo(self) -> None:
        self.tzinfo = datetime.tzinfo()

    def bar(self) -> None:
        self.foo()
