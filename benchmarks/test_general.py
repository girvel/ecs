from ecs import MetasystemFacade, System, Entity


def test_metasystem_facade_add(benchmark):
    def setup():
        ms = MetasystemFacade()

        class ComplexComponent:
            a: int
            b: int
            c: str

        @ms.add
        @System
        def sample_system(_: ComplexComponent):
            ...

        class SampleEntity(Entity):
            def __init__(self):
                self.d = True
                self.e = "abcd"

                self.a = 1
                self.b = 2
                self.c = "abc"

        return (ms, SampleEntity()), {}

    benchmark.pedantic(MetasystemFacade.add, setup=setup, rounds=10_000)
