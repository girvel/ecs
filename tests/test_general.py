from dataclasses import dataclass

import pytest

from ecs import MetasystemFacade, Entity, System


# TODO NEXT type checking
# TODO NEXT github action for tests
@pytest.mark.parametrize("use_dataclass", [
    (False, ),
    (True, ),
])
def test_single_system(use_dataclass):
    processed_entities = []

    ms = MetasystemFacade()

    class Named:
        custom_name: str  # TODO NEXT warnings on type mismatch on debug mode

    @ms.add
    @System
    def process(subject: Named):
        processed_entities.append(subject.custom_name)

    if use_dataclass:
        @dataclass
        class SampleEntity(Entity):
            custom_name: str
    else:
        class SampleEntity(Entity):
            def __init__(self, custom_name: str):
                self.custom_name = custom_name

    ms.add(SampleEntity("Jackie"))
    ms.add(SampleEntity("Hyde"))

    ms.update()

    assert processed_entities == ["Jackie", "Hyde"]
