from .formatting import pretty


class Entity:
    """Entity is a mixture of dict and object.

    You can access attributes as items.
    """

    def __init__(self, attributes):
        """
        Args:
            **attributes: entity's future attributes in format
        """
        self._attributes = attributes

    def __len__(self):
        """Counts number of attributes inside the entity."""
        return len(self._attributes)

    def __repr__(self):
        name = self._attributes.get("name", None)

        return 'Entity{}({})'.format(
            name and f" '{name}'" or "",
            ', '.join(
                f'{key}={pretty(value)}'
                for key, value in self
                if key != 'name'
            )
        )

    def __iter__(self):
        """Iterates entity as pairs: (attribute_name, attribute_value)"""
        yield from self._attributes.items()

    def __contains__(self, item):
        """Checks if entity contains an attribute with the given name."""
        return item in self._attributes

    def __delitem__(self, key):
        """Deletes an attribute with the given name."""
        del self._attributes[key]

    def __getitem__(self, item):
        """Gets an attribute with the given name.

        Args:
            item: a name of the attribute or a tuple (name, default_value)

        Returns:
            Attribute value or default value if specified
        """
        return self._attributes[item]

    def __setitem__(self, item, value):
        """Sets an attribute with the given name."""
        self._attributes[item] = value

    def __delattr__(self, item):
        del self._attributes[item]

    def __getattr__(self, item):
        return self._attributes[item]

    def __setattr__(self, item, value):
        self._attributes[item] = value
