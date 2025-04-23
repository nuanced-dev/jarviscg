from fixtures._utils.parse import (
    parse_into_list_of_expressions,
)


class LazyFrame:
    @classmethod
    def from_list(cls, l):
        return cls(l)

    def __init__(self, l=[]):
        self.ls = l

    def group_by(
        self,
        *by,
        maintain_order,
        **named_by,
    ):
        return parse_into_list_of_expressions(*by, **named_by)
