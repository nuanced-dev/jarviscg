from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

def test_call_graph_generator() -> None:
    entrypoints = [
            "./tests/__init__.py",
            "./tests/fixtures/plugins.py",
            "./tests/fixtures/__init__.py",
            "./tests/fixtures/lazyframe/frame.py",
            "./tests/fixtures/lazyframe/__init__.py",
            "./tests/fixtures/_utils/parse/expr.py",
            "./tests/fixtures/_utils/__init__.py",
            "./tests/fixtures/_utils/parse/__init__.py"
    ]
    expected = {
        "tests": [],
        "tests.fixtures.plugins": [],
        "tests.fixtures": [],
        "tests.fixtures.lazyframe.frame": ["tests.fixtures.lazyframe.frame.LazyFrame"],
        "tests.fixtures.lazyframe.frame.LazyFrame": [],
        "tests.fixtures.lazyframe": [],
        "tests.fixtures._utils.parse.expr": [],
        "tests.fixtures._utils": [],
        "tests.fixtures._utils.parse": [],
        "tests.fixtures.lazyframe.frame.LazyFrame.group_by": ["fixtures._utils.parse.parse_into_list_of_expressions"],
        "fixtures._utils.parse.parse_into_list_of_expressions": [],
        "tests.fixtures.plugins.register_plugin_function": ["fixtures._utils.parse.parse_into_list_of_expressions"],
        "tests.fixtures._utils.parse.expr.parse_into_list_of_expressions": ["tests.fixtures._utils.parse.expr._parse_positional_inputs"],
        "tests.fixtures._utils.parse.expr._parse_positional_inputs": [],
    }

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Simple(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output)
    assert diff == {}
