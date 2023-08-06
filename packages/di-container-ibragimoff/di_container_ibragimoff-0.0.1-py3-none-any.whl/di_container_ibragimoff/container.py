from typing import Any, Callable

from src.di_container_ibragimoff.container_exceptions import FrozenServiceException, UnknownIdentifierException


class Container:
    def __init__(self):
        self._values = {}
        self._frozen: dict[str, bool] = {}
        self._raw = {}

    def get(self, id: str):
        if self._values.get(id) is None:
            raise UnknownIdentifierException()

        if self._raw.get(id) is not None:
            return self._values[id]

        raw = self._values[id]
        val = self._values[id] = self._values[id](self)
        self._raw[id] = raw
        self._frozen[id] = True

        return val

    def set(self, id: str, value: Callable[['Container'], Any]) -> None:
        if self._frozen.get(id):
            raise FrozenServiceException()

        self._values[id] = value

    def has(self, id: str) -> bool:
        return self._values.get(id) is not None


