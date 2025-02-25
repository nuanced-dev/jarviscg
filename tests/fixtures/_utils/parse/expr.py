def parse_into_list_of_expressions(
    *inputs,
    __structify,
    **named_inputs,
) -> list:
    return _parse_positional_inputs(inputs, structify=__structify)

def _parse_positional_inputs(inputs, *, structify) -> list:
    return []
