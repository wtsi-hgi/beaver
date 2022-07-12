from __future__ import annotations

from typing import Set

from beaver.builders.definition import Definition
from beaver.builders.definition.core import DefinitionBuilder
from beaver.db.packages import Package
from beaver.utils.repository import RepositorableObject


class TmpDefinition(Definition):
    def to_repo(self) -> Set[RepositorableObject]:
        return set()

    @staticmethod
    def from_repo(_: RepositorableObject) -> TmpDefinition:
        return TmpDefinition()


class TempBuilder(DefinitionBuilder):
    definition_type = TmpDefinition

    def build(self, _: Set[Package]) -> TmpDefinition:
        return TmpDefinition()
