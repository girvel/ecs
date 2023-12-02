from dataclasses import dataclass

import pytest

from ecs import MetasystemFacade, Entity, System


@pytest.fixture
def name_system_setup():
    processed_entities = []

    ms = MetasystemFacade()

    class Named:
        custom_name: str

    @ms.add
    @System
    def process(subject: Named):
        processed_entities.append(subject.custom_name)

    return ms, processed_entities


@pytest.mark.parametrize(
    "use_dataclass", [False, True]
)
def test_single_system(name_system_setup, use_dataclass):
    ms, processed_entities = name_system_setup

    if use_dataclass:
        @dataclass
        class SampleEntity(Entity):
            custom_name: str
    else:
        class SampleEntity(Entity):
            def __init__(self, custom_name: str):
                self.custom_name = custom_name

    ms.add(SampleEntity("Jackie"))
    hyde = ms.add(SampleEntity("Hyde"))

    ms.update()
    assert processed_entities == ["Jackie", "Hyde"], "Update does not work"

    ms.remove(hyde)
    ms.update()
    assert processed_entities == ["Jackie", "Hyde", "Jackie"], "Removal does not work"


def test_dynamic_distribution(name_system_setup):
    ms, processed_entities = name_system_setup

    class EmptyEntity(Entity): ...

    e = ms.add(EmptyEntity())

    ms.update()
    assert processed_entities == []

    e.custom_name = "Kelso"
    ms.update()
    assert processed_entities == ["Kelso"]

    e.custom_name = "Leo"
    ms.update()
    assert processed_entities == ["Kelso", "Leo"]

    del e.custom_name
    ms.update()
    assert processed_entities == ["Kelso", "Leo"]


def test_yield():
    processed_entities = []

    ms = MetasystemFacade()

    class Component:
        delay: int

    @ms.add
    @System
    def async_process(subject: Component):
        yield from (None for _ in range(subject.delay))
        processed_entities.append(subject.delay)

    class DelayEntity(Entity):
        def __init__(self, delay):
            self.delay = delay

    ms.add(DelayEntity(0))
    ms.add(DelayEntity(1))
    ms.add(DelayEntity(2))

    ms.update()
    assert processed_entities == [0]

    ms.update()
    assert processed_entities == [0, 0, 1]

    ms.update()
    assert processed_entities == [0, 0, 1, 0, 2]
