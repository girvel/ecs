from dataclasses import dataclass

import pytest

from ecs import MetasystemFacade, Entity, System


@pytest.fixture
def sample_setup():
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
def test_single_system(sample_setup, use_dataclass):
    ms, processed_entities = sample_setup

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


@pytest.mark.parametrize(
    "sample_setup", [False, True], indirect=True
)
def test_dynamic_distribution(sample_setup):
    ms, processed_entities = sample_setup

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
    raise NotImplementedError

