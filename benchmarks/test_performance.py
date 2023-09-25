import random

from ecs import Metasystem, create_system, create_multicore_system


def test_update(benchmark):
    ms = Metasystem()

    @ms.add
    @create_system
    def incrementer(e: 'value'):
        e.value += 1

    for _ in range(1_000):
        ms.create(value=random.randrange(1000, 9999))

    @benchmark
    def _():
        ms.update()


def test_multicore_update(benchmark):
    ms = Metasystem()

    @ms.add
    @create_multicore_system
    def incrementer(e: 'value'):
        e.value += 1

    for _ in range(1_000):
        ms.create(value=random.randrange(1000, 9999))

    @benchmark
    def _():
        ms.update()
