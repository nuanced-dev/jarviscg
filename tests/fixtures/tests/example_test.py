import pytest
from tests.fixtures.fixture_class import FixtureClass

@pytest.mark.skip(reason="This is a fixture")
def test_fixture_class_foo_sets_current_time() -> None:
    ins = FixtureClass().foo()

    ins.foo()

    assert ins.current_time
