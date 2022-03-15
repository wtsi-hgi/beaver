"""
        DISCLAIMER

        These types are very much made to work with our use case.
        SQLalchemy is much more generic than this.
        Don't try to reuse these.

"""

from __future__ import annotations

from typing import Any, Generic, List, Type, TypeVar
from sqlalchemy import Column
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Session:
    def query(self, t: Type[T]) -> Query[T]: ...

    def add(self, new: DeclarativeMeta) -> None: ...

    def commit(self) -> None: ...

    def refresh(self, obj: DeclarativeMeta) -> None: ...

class sessionmaker(Session):
    def __init__(
        self,
        bind: Engine = ...,
        autocommit: bool = ..., 
        autoflush: bool = ...
    ) -> None: ...

    def close(self) -> None:
        """generated by sqlalchemy using begin()"""
        ...

T = TypeVar("T", bound=DeclarativeMeta)

class Query(Generic[T]):
    def filter(self, condition: bool) -> Query[T]: ...

    def all(self) -> List[T]: ...

    def with_entities(self, col: Column) -> Query[T]: ...

    def subquery(self) -> Query[T]: ...

    def one(self) -> T: ...

    def count(self) -> int: ...


def relationship(
    o: str,
    back_populates: str = ...,
    foreign_keys: List[Column] = ...,
    uselist: bool = ...
) -> Any: 
    """this was a complete nightmare to work out the
    generic type for, so i gave up"""
    ...