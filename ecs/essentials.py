from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .components import EntityComponent, SystemComponent


def add(system: SystemComponent, entity: EntityComponent) -> None:
    for member_name, requirements in system.ecs_requirements.items():
        if all(hasattr(entity, attribute) for attribute in requirements):
            targets = system.ecs_targets[member_name]
            if entity not in targets:
                targets.append(entity)


def remove(system: SystemComponent, entity: EntityComponent) -> None:
    for targets in system.ecs_targets.values():
        if entity in targets:
            targets.remove(entity)

    # TODO OPT this should be really slow, and using for should only make things worse
    system.ecs_generators = {
        targets: generator
        for targets, generator in system.ecs_generators.items()
        if entity not in targets
    }


def update(system: SystemComponent) -> None:
    for args in itertools.product(*system.ecs_targets.values()):
        system.ecs_process(*args)


def register(
    metasystem: SystemComponent, entity: EntityComponent, *, attribute: Union[str, None] = None
) -> None:
    add(metasystem, entity)
    for system in metasystem.ecs_targets["system"]:
        if (
            attribute is None or
            any(attribute in r for r in system.ecs_requirements.values())  # type: ignore[attr-defined]
        ):
            add(system, entity)  # type: ignore[arg-type]


def unregister(
    metasystem: SystemComponent, entity: EntityComponent, *, attribute: Union[str, None] = None
) -> None:
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
