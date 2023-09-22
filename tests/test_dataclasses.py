from dataclasses import dataclass

import pytest

from ecs import Metasystem, create_system


@pytest.mark.xfail
def test_case():
    processed_entities = []

    ms = Metasystem()

    @dataclass
    class Named(ComponentRequirement("first_name")):
        first_name: str

    @ms.add
    @create_system
    def test_system(entity: Named):
        processed_entities.append(entity.first_name)

    @dataclass
    class ExampleEntity(StaticEntity):
        first_name: str
        age: int = 15

    ms.add(ExampleEntity("Mike"))

    ms.update()
    ms.update()
    assert processed_entities == ['Mike', 'Mike']