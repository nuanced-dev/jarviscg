from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

# Necessary because CallGraphGenerator expects to be running one directory
# up from shallowest module definitions
@pytest.fixture(autouse=True)
def change_directory():
    os.chdir("tests")
    yield
    os.chdir("../")

def test_call_graph_generator_handles_exports() -> None:
    # Fixture setup:
    # - `klass.py` imports `parse_into_list_of_expressions` from `_utils.parse`
    # - `Klass#method` invokes `parse.expr.parse_into_list_of_expressions`
    # - `_utils/parse/__init__.py` exports `parse_into_list_of_expressions`
    # using `__all__`

    entrypoints = [
            "./fixtures/__init__.py",
            "./fixtures/_utils/parse/expr.py",
            "./fixtures/_utils/__init__.py",
            "./fixtures/_utils/parse/__init__.py",
            "./fixtures/core/__init__.py",
            "./fixtures/core/nested/klass.py",
            "./fixtures/core/nested/__init__.py",
    ]
    expected = {
        "fixtures": [],
        "fixtures._utils.parse.expr": [],
        "fixtures._utils": [],
        "fixtures._utils.parse": [],
        "fixtures._utils.parse.expr.parse_into_list_of_expressions": ["fixtures._utils.parse.expr._parse_positional_inputs"],
        "fixtures._utils.parse.parse_into_list_of_expressions": ["fixtures._utils.parse.expr.parse_into_list_of_expressions"],
        "fixtures._utils.parse.expr._parse_positional_inputs": [],
        "fixtures.core.nested.klass": ["fixtures.core.nested.klass.Klass"],
        "fixtures.core.nested.klass.Klass": [],
        "fixtures.core.nested": [],
        "fixtures.core": [],
        "fixtures.core.nested.klass.Klass.method": ["fixtures._utils.parse.parse_into_list_of_expressions"],
    }

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Simple(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output, ignore_order=True)
    assert diff == {}
    assert output["fixtures.core.nested.klass.Klass.method"] == ["fixtures._utils.parse.parse_into_list_of_expressions"]
    assert output["fixtures._utils.parse.parse_into_list_of_expressions"] == ["fixtures._utils.parse.expr.parse_into_list_of_expressions"]
