"""Ecs is an entity-component-system framework that manages the game cycle.

In this interpretation entities are dynamic objects, components are entities'
fields, and systems are functions that take entities as an argument and
brute-force through all their possible combinations. Also, there is a
metasystem, which is a system that launches other systems and is basically a
facade for all important interactions with the game.
"""

from .entity import Entity
from .dynamic_entity import DynamicEntity
from .metasystem import Metasystem, exists
from .static_entity import StaticEntity
from .system import create_system

__all__ = [e.__name__ for e in [
    Entity, DynamicEntity, Metasystem, create_system, exists, StaticEntity,
]]
