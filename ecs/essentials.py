import inspect


def add(system, entity):
    assert all(hasattr(system, a) for a in (
        'process', 'ecs_targets', 'ecs_requirements'
    ))

    for member_name, requirements in system.ecs_requirements.items():
        if all(p in entity for p in requirements):
            targets = system.ecs_targets[member_name]
            if entity not in targets:
                targets.append(entity)


def remove(system, entity):
    for targets in system.ecs_targets.values():
        if entity in targets:
            targets.remove(entity)


def update(system):
    keys = list(system.ecs_targets.keys())

    def _update(members):
        i = len(members)
        if i == len(keys):
            if inspect.isgeneratorfunction(system.process):
                tuple_members = tuple(members.values())
                if tuple_members not in system.ecs_generators:
                    system.ecs_generators[tuple_members] \
                        = system.process(**members)

                try:
                    next(system.ecs_generators[tuple_members])
                except StopIteration:
                    del system.ecs_generators[tuple_members]
            else:
                system.process(**members)
            return

        if len(system.ecs_targets[keys[i]]) > 0:
            for target in system.ecs_targets[keys[i]].copy():
                members[keys[i]] = target
                _update(members)

            del members[keys[i]]

    return _update({})


def register_attribute(metasystem, entity, attribute):
    add(metasystem, entity)
    for system in metasystem.ecs_targets["system"]:
        if any(attribute in r for r in system.ecs_requirements.values()):
            add(system, entity)

    return entity


def unregister_attribute(metasystem, entity, attribute=None):
    systems = [metasystem, *metasystem.ecs_targets["system"]]

    if attribute is None:
        entity.__metasystem__ = None
    else:
        systems = [
            s for s in systems
            if any(
                attribute in r for r in s.ecs_requirements.values()
            )
        ]

    for system in systems:
        remove(system, entity)

    return entity
