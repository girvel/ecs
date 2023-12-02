import functools
import inspect
from typing import Callable, get_type_hints

from ecs import Entity


# TODO NEXT use dataclass with disabled __init__
# TODO NEXT cleanup
class System(Entity):
    name: str
    ecs_process: Callable[..., None]
    ecs_targets: dict[str, list[Entity]]
    ecs_requirements: dict[str, list[str]]
    ecs_generators: dict[tuple, ] | None

    def __init__(self, system_function: Callable[..., None]):
        function_types = get_type_hints(system_function)

        self.name = system_function.__name__

        self.ecs_targets = {
            member_name: [] for member_name in function_types
        }

        self.ecs_requirements = {
            member_name: list(member_type.__annotations__)  # TODO NEXT why get_type_hints here does not work?
            for member_name, member_type
            in function_types.items()
        }

        if inspect.isgeneratorfunction(system_function):
            self.ecs_generators = {}
            self.ecs_process = _generate_async_process(self, system_function)
        else:
            self.ecs_generators = None
            self.ecs_process = system_function


def _generate_async_process(system, system_function):
    @functools.wraps(system_function)
    def result(*args):
        if args not in system.ecs_generators:
            system.ecs_generators[args] = system_function(*args)

        stop_signal = object()
        if next(system.ecs_generators[args], stop_signal) == stop_signal:
            del system.ecs_generators[args]

    return result
