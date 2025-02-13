from deepdiff import DeepDiff
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

def test_nuanced_formatter_includes_filenames() -> None:
    entrypoints = [
        "tests/fixtures/fixture_class.py",
        "tests/fixtures/other_fixture_class.py",
    ]
    expected = {
        "tests.fixtures.fixture_class": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": ["tests.fixtures.fixture_class.FixtureClass"],
        },
        "tests.fixtures.other_fixture_class": {
            "filepath": os.path.abspath("tests/fixtures/other_fixture_class.py"),
            "callees": ["tests.fixtures.other_fixture_class.OtherFixtureClass"],
        },
        "tests.fixtures.other_fixture_class.OtherFixtureClass.baz": {
            "filepath": os.path.abspath("tests/fixtures/other_fixture_class.py"),
            "callees": ["tests.fixtures.fixture_class.FixtureClass.bar", "tests.fixtures.fixture_class.FixtureClass.__init__"],
        },
        "tests.fixtures.fixture_class.FixtureClass.__init__": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": [],
        },
        "tests.fixtures.fixture_class.FixtureClass.bar": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": ["tests.fixtures.fixture_class.FixtureClass.foo"],
        },
        "tests.fixtures.fixture_class.FixtureClass.foo": {
            "filepath": os.path.abspath("tests/fixtures/fixture_class.py"),
            "callees": [],
        }
    }
    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Nuanced(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output, ignore_order=True)
    assert diff == {}
