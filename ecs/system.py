import functools
import inspect
from typing import Callable

from .owned_entity import OwnedEntity


def create_system(protosystem: Callable[..., None]) -> OwnedEntity:
    """Creates system from an annotated function

    Args:
        protosystem: function annotated in ECS style

    Returns:
        New entity with `process`, `ecs_targets` and `ecs_requirements` fields
    """
    result = OwnedEntity(
        name=protosystem.__name__,
        ecs_targets={
            member_name: [] for member_name in protosystem.__annotations__
        },
        ecs_requirements={
            member_name: set(annotation.split(', '))
            for member_name, annotation
            in protosystem.__annotations__.items()
        },
    )

    if inspect.isgeneratorfunction(protosystem):
        result.ecs_generators = {}
        result.process = _generate_async_process(result, protosystem)
    else:
        result.process = protosystem

    return result


def _generate_async_process(system, protosystem):
    @functools.wraps(protosystem)
    def result(*args):
        if args not in system.ecs_generators:
            system.ecs_generators[args] = protosystem(*args)

        try:
            next(system.ecs_generators[args])
        except StopIteration:
            del system.ecs_generators[args]

    return result
