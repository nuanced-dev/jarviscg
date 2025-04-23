from fixtures._utils.parse import parse_into_list_of_expressions
from fixtures.lazyframe import LazyFrame


class Klass():
    def method(self):
        return parse_into_list_of_expressions()

    def other_method(self):
        new_list = list()
        lf = LazyFrame.from_list(new_list)
        return lf.group_by("foo", maintain_order=False, __structify=False)
