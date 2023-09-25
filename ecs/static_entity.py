from ecs.formatting import pretty


class StaticError(Exception): pass

class StaticEntity:
    """StaticEntity is an Entity with fixed amount of attributes.

    You can add new attributes, but it will not cause addition/removal from systems. StaticEntity is registered in
    systems only when it is added to the Metasystem and it is unregistered only when it is removed from the Metasystem.
    """

    def __getitem__(self, item):
        """Gets an attribute with the given name.

        Args:
            item: a name of the attribute or a tuple (name, default_value)

        Returns:
            Attribute value or default value if specified
        """
        return getattr(self, item)

    def __setitem__(self, item, value):
        """Sets an attribute with the given name."""
        return setattr(self, item, value)

    def __contains__(self, item):
        """Checks if entity contains an attribute with the given name."""
        return hasattr(self, item)

    def __len__(self):
        """Counts number of attributes inside the entity."""
        return len(list(self.__iter__()))

    def __repr__(self):
        name = self["name", None]

        return 'StaticEntity{}({})'.format(
            name and f" '{name}'" or "",
            ', '.join(
                f'{key}={pretty(value)}'
                for key, value in self
                if key != 'name'
            )
        )

    def __iter__(self):
        """Iterates entity as pairs: (attribute_name, attribute_value)"""

        for name, value in vars(self).items():
            if not name.startswith('__') or not name.endswith('__'):
                yield name, value