import functools
import inspect
from typing import Callable, get_type_hints, cast, List, Dict, Tuple, Iterator, Union

from .entity import Entity


# TODO NEXT use dataclass with disabled __init__
# TODO NEXT cleanup
class System(Entity):
    name: str
    ecs_process: Callable[..., None]
    ecs_targets: Dict[str, List[Entity]]
    ecs_requirements: Dict[str, List[str]]
    ecs_generators: Dict[Tuple[Entity, ...], Iterator[None]]

    def __init__(self, system_function: Union[Callable[..., Iterator[None]], None]):
        function_types = get_type_hints(system_function)
        if "return" in function_types:
            del function_types["return"]

        self.name = system_function.__name__
        self.ecs_generators = {}

        self.ecs_targets = {
            member_name: [] for member_name in function_types
        }

        self.ecs_requirements = {
            member_name: list(member_type.__annotations__)  # TODO NEXT why get_type_hints here does not work?
            for member_name, member_type
            in function_types.items()
        }

        if inspect.isgeneratorfunction(system_function):
            self.ecs_process = _generate_async_process(self, system_function)
        else:
            self.ecs_process = cast(Callable[..., None], system_function)


def _generate_async_process(system: System, system_function: Callable[..., Iterator[None]]) -> Callable[..., None]:
    @functools.wraps(system_function)
    def result(*args: Entity) -> None:
        if args not in system.ecs_generators:
            system.ecs_generators[args] = system_function(*args)

        stop_signal = object()
        if next(system.ecs_generators[args], stop_signal) == stop_signal:
            del system.ecs_generators[args]

    return result
