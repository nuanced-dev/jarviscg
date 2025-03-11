from fixtures.fixture_class import FixtureClass as AliasedFixtureClass

class OtherFixtureClass():
    def baz(self) -> None:
        ins = AliasedFixtureClass()
        ins.bar()
