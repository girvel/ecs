from ecs import MetasystemFacade, Entity, System


# TODO NEXT type checking
# TODO NEXT github action for tests
def test_single_system():
    processed_entities = []

    ms = MetasystemFacade()

    class Named:
        custom_name: str  # TODO NEXT warnings on type mismatch on debug mode

    @ms.add
    @System
    def process(subject: Named):
        processed_entities.append(subject.custom_name)

    class SampleEntity(Entity):  # TODO NEXT test for dataclass
        def __init__(self, custom_name: str):
            self.custom_name = custom_name

    ms.add(SampleEntity("Jackie"))
    ms.add(SampleEntity("Hyde"))

    ms.update()

    assert processed_entities == ["Jackie", "Hyde"]
