from __future__ import annotations

import abc
from typing import Set

from beaver.utils.repository import RepositorableObject


class Definition(abc.ABC):
    
    @abc.abstractmethod
    def to_repo(self) -> Set[RepositorableObject]:
        ...

    @staticmethod
    @abc.abstractstaticmethod
    def from_repo(_: RepositorableObject) -> Definition:
        ...
