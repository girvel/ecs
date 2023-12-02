from ecs import MetasystemFacade, System, Entity


def test_generator_memory_leak():
    ms = MetasystemFacade()

    class AsyncTriggerComponent:
        async_trigger_flag: None

    @ms.add
    @System
    def async_system(_: AsyncTriggerComponent):
        yield
        yield

    class AsyncTrigger(Entity):
        def __init__(self):
            self.async_trigger_flag = None

    trigger = ms.add(AsyncTrigger())
    ms.update()
    ms.remove(trigger)

    assert len(async_system.ecs_generators) == 0
