from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg import formats
from jarviscg.core import CallGraphGenerator
from jarviscg.processing.extProcessor import ExtProcessor


def test_call_graph_generator_includes_calls_to_methods_of_aliased_module() -> None:
    # Fixture setup:
    # - `fixtures/lazyframe/__init__.py` exports `*`
    # - `klass.py` imports `LazyFrame` from `fixtures`
    # - `Klass#other_method` invokes `LazyFrame.from_list` class method and
    # `LazyFrame#group_by` instance method
    entrypoints = [
            "./tests/__init__.py",
            "./tests/fixtures/__init__.py",
            "./tests/fixtures/lazyframe/__init__.py",
            "./tests/fixtures/lazyframe/frame.py",
            "./tests/fixtures/core/__init__.py",
            "./tests/fixtures/core/nested/klass.py",
            "./tests/fixtures/core/nested/__init__.py",
    ]
    package = "tests"
    caller = "fixtures.core.nested.klass.Klass.other_method"
    invoked_class_method = "fixtures.lazyframe.frame.LazyFrame.from_list"
    invoked_instance_method = "fixtures.lazyframe.frame.LazyFrame.group_by"
    cg = CallGraphGenerator(entrypoints, package)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    for callee in [invoked_class_method, invoked_instance_method]:
        assert callee in output[caller]

def test_call_graph_generator_includes_aliased_functions() -> None:
    # Fixture setup:
    # - `klass.py` imports `parse_into_list_of_expressions` from `_utils.parse`
    # - `Klass#method` invokes `parse.expr.parse_into_list_of_expressions`
    # - `_utils/parse/__init__.py` exports `parse_into_list_of_expressions`
    # using `__all__`

    entrypoints = [
            "./tests/__init__.py",
            "./tests/fixtures/__init__.py",
            "./tests/fixtures/_utils/parse/expr.py",
            "./tests/fixtures/_utils/__init__.py",
            "./tests/fixtures/_utils/parse/__init__.py",
            "./tests/fixtures/core/__init__.py",
            "./tests/fixtures/core/nested/klass.py",
            "./tests/fixtures/core/nested/__init__.py",
    ]
    package = "tests"
    cg = CallGraphGenerator(entrypoints, package)
    cg.analyze()

    formatter = formats.Simple(cg)
    output = formatter.generate()

    assert output["fixtures.core.nested.klass.Klass.method"] == ["fixtures._utils.parse.expr.parse_into_list_of_expressions"]
    assert output["fixtures._utils.parse.expr.parse_into_list_of_expressions"] == ["fixtures._utils.parse.expr._parse_positional_inputs"]

def test_call_graph_generator_includes_refs_to_aliased_classes() -> None:
    caller_of_aliased_class = "fixtures.other_fixture_class.OtherFixtureClass.baz"
    package = "tests"
    entrypoints = [
        "./tests/fixtures/__init__.py",
        "./tests/fixtures/fixture_class.py",
        "./tests/fixtures/other_fixture_class.py",
    ]

    cg = CallGraphGenerator(entrypoints, package)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    assert "fixtures.fixture_class.FixtureClass.bar" in output[caller_of_aliased_class]
    assert "fixtures.fixture_class.FixtureClass.bar" in output.keys()

def test_call_graph_generator_default_builds_complete_graph_for_pytest_file() -> None:
    package = "tests"
    entrypoints = [
        "./tests/fixtures/tests/__init__.py",
        "./tests/fixtures/tests/example_test.py",
        "./tests/fixtures/fixture_class.py",
    ]
    expected_callees = [
        "fixtures.fixture_class.FixtureClass.__init__",
        "fixtures.fixture_class.FixtureClass.foo",
        "tests.fixtures.fixture_class.FixtureClass",
    ]

    cg = CallGraphGenerator(entrypoints, package)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    test_function_callees = output["fixtures.tests.example_test.test_fixture_class_foo_sets_current_time"]
    assert "tests.fixtures.fixture_class.FixtureClass" in output.keys()
    for callee in expected_callees:
        assert callee in test_function_callees

def test_call_graph_generator_dependency_analysis_disabled() -> None:
    package = "tests"
    entrypoints = [
        "./tests/fixtures/fixture_class.py",
        "./tests/fixtures/__init__.py",
        "./tests/__init__.py",
    ]
    dependency_called_function_name = "functools.cache"
    dependency_called_attribute_name1 = "datetime.datetime.now"
    dependency_called_attribute_name2 = "multiprocessing.Pipe"
    imported_called_name = "multiprocessing.Process"
    expected_callees = [
        dependency_called_attribute_name1,
        dependency_called_attribute_name2,
        imported_called_name,
        dependency_called_function_name,
    ]

    cg = CallGraphGenerator(entrypoints, package)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    callees = output["fixtures.fixture_class.FixtureClass.foo"]
    assert output[dependency_called_function_name] == []
    for callee in expected_callees:
        assert callee in callees


def test_call_graph_generator_dependency_analysis_enabled() -> None:
    package = "tests"
    entrypoints = [
        "./tests/fixtures/fixture_class.py",
        "./tests/fixtures/__init__.py",
        "./tests/__init__.py",
    ]
    dependency_called_function_name = "functools.cache"
    dependency_called_attribute_name1 = "datetime.datetime.now"
    dependency_called_attribute_name2 = "multiprocessing.Pipe"
    imported_called_name = "multiprocessing.Process"

    cg = CallGraphGenerator(entrypoints, package, decy=True)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    callees = output["fixtures.fixture_class.FixtureClass.foo"]
    assert dependency_called_attribute_name1 not in callees
    assert dependency_called_attribute_name2 not in callees
    assert imported_called_name not in callees
    assert dependency_called_function_name in callees
    assert len(output[dependency_called_function_name]) > 0
