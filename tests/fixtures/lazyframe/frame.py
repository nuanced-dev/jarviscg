from fixtures._utils.parse import (
    parse_into_list_of_expressions,
)

class LazyFrame:
    def group_by(
        self,
        *by,
        maintain_order,
        **named_by,
    ):
        return parse_into_list_of_expressions(*by, **named_by)
