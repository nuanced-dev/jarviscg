import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

def test_nuanced_formatter_includes_filenames() -> None:
    entrypoints = [
        "tests/fixtures/fixture_class.py",
        "tests/fixtures/other_fixture_class.py",
    ]
    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    formatter = formats.Nuanced(cg)
    output = formatter.generate()

    assert output["tests.fixtures.fixture_class.FixtureClass.bar"]["filepath"] == os.abspath("tests/fixtures/fixture_class.py")
    assert output["tests.fixtures.fixture_class.FixtureClass.bar"]["callees"] == ["tests.fixtures.fixture_class.FixtureClass.foo"]
