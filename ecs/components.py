import sys
from typing import Callable, Dict, List, Tuple, Iterator, Union

if sys.version_info < (3, 8):
    from typing import TypeVar

    T = TypeVar("T")

    def runtime_checkable(x: T) -> T:
        return x

    Protocol = object
else:
    from typing import runtime_checkable, Protocol


@runtime_checkable
class EntityComponent(Protocol):
    __metasystem__: "Union[SystemComponent, None]"

@runtime_checkable
class SystemComponent(Protocol):
    ecs_process: Callable[..., None]
    ecs_targets: Dict[str, List[EntityComponent]]
    ecs_requirements: Dict[str, List[str]]
    ecs_generators: Dict[Tuple[EntityComponent, ...], Iterator[None]]
