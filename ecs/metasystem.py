from typing import TypeVar

from .entity import Entity

from .essentials import update, register, unregister
from .system import System


_TEntity = TypeVar("_TEntity", bound=Entity)


class MetasystemFacade(Entity):
    """Facade class containing all general ECS logic."""

    __metasystem__: System
    ecs_metasystem_facade_flag: None = None

    def __init__(self) -> None:
        """Initializes a new game; creates a metasystem."""

        @System
        def metasystem(system: System) -> None:
            update(system)

        self.__metasystem__ = metasystem

    def add(self, entity: _TEntity) -> _TEntity:
        """Registers entity as a member of ECS; sets entity's __metasystem__ attribute.

        Args:
            entity: entity to be added

        Returns:
            The same entity
        """

        if entity.__metasystem__ is not None:
            raise OwnershipException("Entity {entity} already belongs to a metasystem")

        entity.__metasystem__ = self.__metasystem__

        register(self.__metasystem__, entity)

        return entity

    def remove(self, entity: _TEntity) -> _TEntity:
        """Unregisters entity from the ECS.

        Args:
            entity: entity to be added

        Returns:
            The same entity
        """

        if entity.__metasystem__ is None:
            raise OwnershipException("Entity should belong to the metasystem to be deleted from it")

        unregister(self.__metasystem__, entity)
        return entity

    def update(self) -> None:
        """Updates all the systems once."""
        update(self.__metasystem__)

    def register_itself(self) -> None:
        """Allows system to access MetasystemFacade as entity. Call after adding systems."""
        register(self.__metasystem__, self)


class OwnershipException(Exception):
    pass


def exists(entity: "Entity") -> bool:
    """Determines whether the entity belongs to any ECS."""
    return entity.__metasystem__ is not None
