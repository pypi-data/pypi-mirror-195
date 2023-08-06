from typing import Any, Callable

from di_container_ibragimoff.container_exceptions import FrozenServiceException, UnknownIdentifierException, \
    TagAlreadyRegisteredForTheService


class Container:
    def __init__(self):
        self._values: dict[str, Callable[['Container'], Any]] = {}
        self._initialized: dict[str, Any] = {}
        self._tags: dict[str, list[str]] = {}

    def get(self, id: str):
        if self._values.get(id) is None:
            raise UnknownIdentifierException()

        if self._initialized.get(id) is not None:
            return self._initialized[id]

        val = self._initialized[id] = self._values[id](self)

        return val

    def set(self, id: str, value: Callable[['Container'], Any]) -> None:
        if self._initialized.get(id) is not None:
            raise FrozenServiceException()

        self._values[id] = value

    def set_tag(self, id: str, tag: str) -> None:
        if self._values.get(id) is None:
            raise UnknownIdentifierException()

        if self._tags.get(tag) is not None and id in self._tags[tag]:
            raise TagAlreadyRegisteredForTheService()

        if self._tags.get(tag) is not None:
            self._tags[tag].append(id)
            return

        self._tags[tag] = [id]

    def find_ids_by_tag(self, tag: str) -> list[str] | None:
        return self._tags.get(tag)

    def extends(self, id: str, extension: Callable[['Container', Any], Any]) -> None:
        if self._initialized.get(id) is not None:
            raise FrozenServiceException(id)
        if self._values.get(id) is None:
            raise UnknownIdentifierException(id)

        definition = self._values[id]
        self._values[id] = lambda c: extension(c, definition(c))

    def has(self, id: str) -> bool:
        return self._values.get(id) is not None
