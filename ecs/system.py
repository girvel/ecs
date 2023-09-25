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
    return _create_system(protosystem, False)


def create_multicore_system(protosystem: Callable[..., None]) -> OwnedEntity:
    """Creates system from an annotated function, that will use multiprocessing

    Args:
        protosystem: function annotated in ECS style

    Returns:
        New entity with `process`, `ecs_targets` and `ecs_requirements` fields
    """
    return _create_system(protosystem, True)


def _create_system(protosystem, multicore):
    result = OwnedEntity(
        name=protosystem.__name__,
        process=protosystem,
        ecs_targets={
            member_name: [] for member_name in protosystem.__annotations__
        },
        ecs_requirements={
            member_name: set(annotation.split(', '))
            for member_name, annotation
            in protosystem.__annotations__.items()
        },
        multicore=multicore
    )

    if inspect.isgeneratorfunction(protosystem):
        result.ecs_generators = {}

    return result
