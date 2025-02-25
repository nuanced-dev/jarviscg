from deepdiff import DeepDiff
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

@pytest.fixture(autouse=True)
def teardown():
    yield
    os.chdir("../")

def test_nuanced_formatter_includes_filenames() -> None:
    os.chdir("tests")
    entrypoints = [
        "./fixtures/fixture_class.py",
        "./fixtures/other_fixture_class.py",
    ]
    expected = {
        "fixtures.fixture_class": {
            "filepath": os.path.abspath("fixtures/fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass"],
        },
        "fixtures.other_fixture_class": {
            "filepath": os.path.abspath("fixtures/other_fixture_class.py"),
            "callees": ["fixtures.other_fixture_class.OtherFixtureClass"],
        },
        "fixtures.other_fixture_class.OtherFixtureClass.baz": {
            "filepath": os.path.abspath("fixtures/other_fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass.bar", "fixtures.fixture_class.FixtureClass.__init__"],
        },
        "fixtures.fixture_class.FixtureClass.__init__": {
            "filepath": os.path.abspath("fixtures/fixture_class.py"),
            "callees": [],
        },
        "fixtures.fixture_class.FixtureClass.bar": {
            "filepath": os.path.abspath("fixtures/fixture_class.py"),
            "callees": ["fixtures.fixture_class.FixtureClass.foo"],
        },
        "fixtures.fixture_class.FixtureClass.foo": {
            "filepath": os.path.abspath("fixtures/fixture_class.py"),
            "callees": [],
        }
    }
    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Nuanced(cg)
    output = formatter.generate()

    diff = DeepDiff(expected, output, ignore_order=True)
    assert diff == {}
