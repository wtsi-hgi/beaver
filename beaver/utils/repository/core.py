import abc

from beaver.utils.repository import RepositorableObject


class Repository(abc.ABC):
    @abc.abstractmethod
    def get(self, _: str) -> RepositorableObject:
        ...

    @abc.abstractmethod
    def add(self, _: RepositorableObject) -> None:
        ...
