from typing import TypeVar

from .system import System
from .entity import Entity

from .essentials import update, register, unregister
from .components import SystemComponent, EntityComponent


_TEntity = TypeVar("_TEntity", bound=Entity)


class MetasystemFacade:
    """Facade class containing all general ECS logic."""

    _metasystem: System

    def __init__(self) -> None:
        """Initializes a new game; creates a metasystem."""

        @System
        def metasystem(system: SystemComponent) -> None:
            update(system)

        self._metasystem = metasystem

    def add(self, entity: _TEntity) -> _TEntity:
        """Registers entity as a member of ECS; sets entity's __metasystem__ attribute.

        Args:
            entity: entity to be added

        Returns:
            The same entity
        """

        if entity.__metasystem__ is not None:
            raise OwnershipException("Entity {entity} already belongs to a metasystem")

        entity.__metasystem__ = self._metasystem

        register(self._metasystem, entity)

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

        unregister(self._metasystem, entity)
        return entity

    def update(self) -> None:
        """Updates all the systems once."""
        update(self._metasystem)


class OwnershipException(Exception):
    pass


def exists(entity: EntityComponent) -> bool:
    """Determines whether the entity belongs to any ECS."""
    return entity.__metasystem__ is not None
