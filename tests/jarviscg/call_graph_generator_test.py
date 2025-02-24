from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

def test_call_graph_generator() -> None:
    entrypoints = [
            os.path.abspath("fixtures/__init__.py"),
            os.path.abspath("fixtures/plugins.py"),
            os.path.abspath("fixtures/lazyframe/frame.py"),
            os.path.abspath("fixtures/lazyframe/__init__.py"),
            os.path.abspath("fixtures/_utils/parse/expr.py"),
            os.path.abspath("fixtures/_utils/__init__.py"),
            os.path.abspath("fixtures/_utils/parse/__init__.py")
    ]
    expected = {}

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Simple(cg)
    output = formatter.generate()

    assert output["fixtures._utils.parse.expr.parse_into_list_of_expressions"]
    assert "fixtures._utils.parse.expr.parse_into_list_of_expressions" in output["fixtures.plugins.register_plugin_function"]
