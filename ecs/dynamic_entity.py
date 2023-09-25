from .entity import Entity
from .essentials import register_attribute, unregister_attribute


class DynamicEntity(Entity):
    """Represents an entity that belongs to some metasystem."""

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if '__metasystem__' in self:
            register_attribute(self.__metasystem__, self, key)

    def __delattr__(self, item):
        super().__delattr__(item)
        if '__metasystem__' in self:
            unregister_attribute(self.__metasystem__, self, item)
