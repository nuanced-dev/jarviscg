from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

@pytest.fixture(autouse=True)
def teardown():
    yield
    os.chdir("../")

def test_call_graph_generator() -> None:
    os.chdir("tests")
    entrypoints = [
            "./fixtures/plugins.py",
            "./fixtures/__init__.py",
            "./fixtures/lazyframe/frame.py",
            "./fixtures/lazyframe/__init__.py",
            "./fixtures/_utils/parse/expr.py",
            "./fixtures/_utils/__init__.py",
            "./fixtures/_utils/parse/__init__.py",
    ]
    expected = {
        "fixtures.plugins": [],
        "fixtures": [],
        "fixtures.lazyframe.frame": ["fixtures.lazyframe.frame.LazyFrame"],
        "fixtures.lazyframe.frame.LazyFrame": [],
        "fixtures.lazyframe": [],
        "fixtures._utils.parse.expr": [],
        "fixtures._utils": [],
        "fixtures._utils.parse": [],
        "fixtures.lazyframe.frame.LazyFrame.group_by": ["fixtures._utils.parse.expr.parse_into_list_of_expressions"],
        "fixtures.plugins.register_plugin_function": ["fixtures._utils.parse.expr.parse_into_list_of_expressions"],
        "fixtures._utils.parse.expr.parse_into_list_of_expressions": ["fixtures._utils.parse.expr._parse_positional_inputs"],
        "fixtures._utils.parse.expr._parse_positional_inputs": [],
    }

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Simple(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output)
    assert diff == {}
