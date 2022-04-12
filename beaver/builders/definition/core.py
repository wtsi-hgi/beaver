import abc
from typing import Set, Type
from beaver.builders.definition import Definition

from beaver.db.packages import Package


class DefinitionBuilder(abc.ABC):

    definition_type: Type[Definition]

    @abc.abstractmethod
    def build(self, _: Set[Package]) ->  Definition:
        ...