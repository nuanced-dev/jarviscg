from deepdiff import DeepDiff
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats


def test_nuanced_formatter_formats_graph() -> None:
    entrypoints = [
        "./tests/fixtures/fixture_class.py",
        "./tests/fixtures/other_fixture_class.py",
    ]
    expected = {
        "fixtures.fixture_class": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass"],
            "lineno": 1,
            "end_lineno": 13
        },
        "fixtures.other_fixture_class": {
            "filepath": os.path.abspath("tests/fixtures/other_fixture_class.py"),
            "callees": ["fixtures.other_fixture_class.OtherFixtureClass", "fixtures.fixture_class"],
            "lineno": 1,
            "end_lineno": 6
        },
        "fixtures.other_fixture_class.OtherFixtureClass.baz": {
            "filepath": os.path.abspath("tests/fixtures/other_fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass.bar", "fixtures.fixture_class.FixtureClass.__init__"],
            "lineno": 4,
            "end_lineno": 6
        },
        "fixtures.fixture_class.FixtureClass.__init__": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": [],
            "lineno": 5,
            "end_lineno": 6
        },
        "fixtures.fixture_class.FixtureClass.bar": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass.foo"],
            "lineno": 12,
            "end_lineno": 13
        },
        "fixtures.fixture_class.FixtureClass.foo": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": [],
            "lineno": 8,
            "end_lineno": 10
        }
    }
    cg = CallGraphGenerator(entrypoints, "tests")
    cg.analyze()

    formatter = formats.Nuanced(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output, ignore_order=True)
    assert diff == {}
