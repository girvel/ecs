from .entity import Entity
from .essentials import update, register_attribute, unregister_attribute
from .owned_entity import OwnedEntity, OwnershipException


class Metasystem(Entity):
    """Metasystem is a system that brute-forces systems and a facade to all
    interactions with the game.
    """

    def __init__(self):
        self.ecs_targets = {'system': [],}
        self.ecs_requirements = {
            'system': {'process', 'ecs_requirements', 'ecs_targets'}
        }
        self.name = 'metasystem'

    def process(self, system):
        update(system)

    def create(self, **attributes):
        """Creates in-game entity.

        Args:
            **attributes: attributes (components) that entity will contain

        Returns:
            In-game entity
        """

        return self.add(OwnedEntity(**attributes))

    def add(self, entity):
        """Adds an entity to the metasystem; adds __metasystem__ attribute."""

        if '__metasystem__' in entity:
            raise OwnershipException(
                "Entity {entity} is already belongs to a metasystem"
            )

        entity.__metasystem__ = self

        for attribute, _ in entity:
            register_attribute(self, entity, attribute)

        return entity

    def delete(self, entity):
        """Removes entity from the game.

        Args:
            entity: in-game entity to be removed
        """

        unregister_attribute(self, entity)

    def update(self):
        """Updates all the systems once."""

        update(self)