from typing import Callable, get_type_hints

from ecs import Entity


# TODO NEXT use dataclass with disabled __init__
# TODO NEXT cleanup
class System(Entity):
    name: str
    ecs_process: Callable[..., None]
    ecs_targets: dict[str, list[Entity]]
    ecs_requirements: dict[str, list[str]]

    def __init__(self, system_function: Callable[[...], None]):
        function_types = get_type_hints(system_function)

        self.name = system_function.__name__
        self.ecs_process = system_function
        self.ecs_targets = {
            member_name: [] for member_name in function_types
        }
        self.ecs_requirements = {
            member_name: list(member_type.__annotations__)  # TODO NEXT why get_type_hints here does not work?
            for member_name, member_type
            in function_types.items()
        }


# def create_system(protosystem: Callable[..., None]) -> DynamicEntity:
#     """Creates system from an annotated function
#
#     Args:
#         protosystem: function annotated in ECS style
#
#     Returns:
#         New entity with `process`, `ecs_targets` and `ecs_requirements` fields
#     """
#     result = DynamicEntity(
#         name=protosystem.__name__,
#         ecs_targets={
#             member_name: [] for member_name in protosystem.__annotations__
#         },
#         ecs_requirements={
#             member_name: set(annotation.split(', '))
#             for member_name, annotation
#             in protosystem.__annotations__.items()
#         },
#     )
#
#     if inspect.isgeneratorfunction(protosystem):
#         result.ecs_generators = {}
#         result.process = _generate_async_process(result, protosystem)
#     else:
#         result.process = protosystem
#
#     return result
#
#
# def _generate_async_process(system, protosystem):
#     @functools.wraps(protosystem)
#     def result(*args):
#         if args not in system.ecs_generators:
#             system.ecs_generators[args] = protosystem(*args)
#
#         try:
#             next(system.ecs_generators[args])
#         except StopIteration:
#             del system.ecs_generators[args]
#
#     return result
