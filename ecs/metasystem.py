from typing import TypeVar

from ecs import Entity

from .essentials import update, register_attribute, unregister_attribute
from .system import System


_TEntity = TypeVar("_TEntity", bound=Entity)


# TODO NEXT rename to MicroEngine?
class MetasystemFacade:
    """Facade for a metasystem and all interactions with the game."""
    _metasystem: System

    def __init__(self):
        """Initializes a new game; creates a metasystem."""

        @System
        def metasystem(system: System):
            update(system)

        self._metasystem = metasystem  # TODO NEXT as a staticmethod?

    def add(self, entity: _TEntity) -> _TEntity:
        """Adds an entity to the metasystem; adds __metasystem__ attribute.

        Args:
            entity: entity to be added

        Returns:
            The same entity
        """

        if entity.__metasystem__ is not None:
            raise OwnershipException(
                "Entity {entity} is already belongs to a metasystem"
            )

        entity.__metasystem__ = self._metasystem

        for attribute in dir(entity):
            if attribute.startswith('__') and attribute.endswith('__'): continue
            register_attribute(self._metasystem, entity, attribute)
            # TODO NEXT remove for, just a call with attribute=None should be faster & cleaner

        return entity

    def remove(self, entity: _TEntity) -> _TEntity:
        """Removes entity from the game.

        Args:
            entity: in-game entity to be removed
        """

        if entity.__metasystem__ is None:
            raise OwnershipException("Entity should belong to the metasystem to be deleted from it")

        unregister_attribute(self._metasystem, entity)
        return entity

    def update(self) -> None:
        """Updates all the systems once."""
        update(self._metasystem)


class OwnershipException(Exception):
    pass


def exists(entity: "Entity") -> bool:
    """Determines whether entity belongs to any metasystem."""
    return entity.__metasystem__ is not None
