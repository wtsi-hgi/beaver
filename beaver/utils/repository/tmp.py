from beaver.utils.repository import RepositorableObject
from beaver.utils.repository.core import Repository

class TempRepository(Repository):
    def add(self, _: RepositorableObject) -> None:
        ...

    def get(self, _: str) -> RepositorableObject:
        return RepositorableObject()