from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .entity import Entity
    from .system import System


def add(system: "System", entity: "Entity") -> None:
    """Tries to register entity as a system target.

    Succeeds if entity has all the required fields to be a target for the
    system (they are listed in system.ecs_requirements[target_name]). Success
    means that the next iteration of the system will use entity one or multiple
    times.
    """

    for member_name, requirements in system.ecs_requirements.items():
        if all(hasattr(entity, attribute) for attribute in requirements):
            targets = system.ecs_targets[member_name]
            if entity not in targets:
                targets.append(entity)


def remove(system: "System", entity: "Entity") -> None:
    """Tries to unregister entity from a system.

    Guarantees that the entity will no longer be processed by the system.
    """

    for targets in system.ecs_targets.values():
        if entity in targets:
            targets.remove(entity)


def update(system: "System") -> None:
    """Launches a system one time.

    Calls a system.ecs_process with each possible combination of targets.
    """

    for args in itertools.product(*system.ecs_targets.values()):
        system.ecs_process(*args)


# TODO NEXT rename to register & unregister?
def register_attribute(
    metasystem: "System", entity: "Entity", attribute: str
) -> None:
    """Notifies systems that the entity gained new attribute.

    Args:
        metasystem: metasystem itself, not a facade
        entity: entity that gained new attribute
        attribute: name of the attribute
    """

    add(metasystem, entity)
    for system in metasystem.ecs_targets["system"]:
        if any(attribute in r for r in system.ecs_requirements.values()):  # type: ignore[attr-defined]
            add(system, entity)  # type: ignore[arg-type]


def unregister_attribute(
    metasystem: "System", entity: "Entity", attribute: Union[str, None] = None
) -> None:
    """Notifies systems that entity lost an attribute or that entity itself
    should be deleted.

    Args:
        metasystem: metasystem itself, not a facade
        entity: entity that lost an attribute or should be deleted
        attribute: name of the attribute or None if entity itself should be deleted
    """

    systems = [metasystem, *metasystem.ecs_targets["system"]]

    if attribute is None:
        entity.__metasystem__ = None
    else:
        systems = [
            s for s in systems
            if any(attribute in r for r in s.ecs_requirements.values())  # type: ignore[attr-defined]
        ]

    for system in systems:
        remove(system, entity)  # type: ignore[arg-type]
