import random
from dataclasses import dataclass

import pytest

from ecs import Metasystem, create_system, Entity, StaticEntity


@dataclass
class StaticExample(StaticEntity):
    value: int


@pytest.mark.parametrize("entity_type", [Entity, StaticExample])
def test_update(benchmark, entity_type):
    ms = Metasystem()

    @ms.add
    @create_system
    def incrementer(e: 'value'):
        e.value += 1

    for _ in range(1_000):
        ms.add(entity_type(value=random.randrange(1000, 9999)))

    @benchmark
    def _():
        ms.update()
