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

def test_call_graph_generator_processes_files_depth_first() -> None:
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

    diff = DeepDiff(expected, output, ignore_order=True)
    assert diff == {}

def test_call_graph_generator_generates_broken_graph() -> None:
    # Explaining this test:
    # - `klass.py` imports `parse_into_list_of_expressions` from `_utils.parse`
    # - `Klass#method` invokes `parse.expr.parse_into_list_of_expressions`
    # - `_utils/parse/__init__.py` exports `parse_into_list_of_expressions`

    # When the `core.nested` module is processed by CallGraphGenerator before the
    # `_utils.parse` module, the graph that is generated refers to
    # `parse_into_list_of_expressions` by two different fully qualified names:
    # `_utils.parse.expr.parse_into_list_of_expressions` and
    # `_utils.parse.parse_into_list_of_expressions`
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
        "fixtures._utils.parse.parse_into_list_of_expressions": [],
        "fixtures._utils.parse.expr.parse_into_list_of_expressions": ["fixtures._utils.parse.expr._parse_positional_inputs"],
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
    assert output["fixtures._utils.parse.parse_into_list_of_expressions"] == []
    assert output["fixtures._utils.parse.expr.parse_into_list_of_expressions"] == ["fixtures._utils.parse.expr._parse_positional_inputs"]
