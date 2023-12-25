"""Ecs is an entity-component-system framework that manages the game cycle.

In this interpretation entities are dynamic objects, components are attributes,
and systems are functions that take entities as an argument and
brute-force through all their possible combinations. Also, there is a
metasystem, which is a system that launches other systems and is basically a
facade for all important interactions with the game.
"""
# TODO NEXT rewrite this doc

from .entity import Entity
from .metasystem import MetasystemFacade, exists
from .system import System

__all__ = [e.__name__ for e in [  # type: ignore[attr-defined]
    Entity, System, MetasystemFacade, exists,
]]
