from typing import Any, TYPE_CHECKING, Union

from .essentials import register, unregister

if TYPE_CHECKING:
    from .system import System


class Entity:
    """Represents an entity that belongs to some metasystem."""
    __metasystem__: "Union[System, None]" = None

    def __setattr__(self, key: str, value: Any) -> None:
        is_new = not hasattr(self, key)

        super().__setattr__(key, value)

        if self.__metasystem__ is not None and is_new:
            register(self.__metasystem__, self, attribute=key)

    def __delattr__(self, item: str) -> None:
        super().__delattr__(item)
        if self.__metasystem__ is not None:
            unregister(self.__metasystem__, self, attribute=item)
