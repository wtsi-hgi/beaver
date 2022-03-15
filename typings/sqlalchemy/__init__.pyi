"""
        DISCLAIMER

        These types are very much made to work with our use case.
        SQLalchemy is much more generic than this.
        Don't try to reuse these.

"""

from __future__ import annotations
import enum
from typing import Dict, Any, Type, TypeVar

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query
from sqlalchemy.orm.decl_api import DeclarativeMeta

class ForeignKey:
    def __init__(self, col: str) -> None: ...

def create_engine(url: str, connect_args: Dict[str, Any]) -> Engine: ...

class ColType: ...

class ColVal: ...

C = TypeVar("C", bound=DeclarativeMeta)

class Column:
    def __init__(self,
        col_type: Type[ColType] | ColVal,
        fk: ForeignKey = ...,
        primary_key: bool = ..., 
        autoincrement: bool = ..., 
        nullable: bool = ...,
        default: Any = ...) -> None:
        ...

    def __eq__(self, __o: object) -> bool: ...

    def __gt__(self, o: object) -> bool: ...

    @classmethod
    def in_(cls, subquery: Query[C]) -> bool: ...



class String(ColType): ...

class Integer(ColType): ...

class DateTime(ColType): ...

class Boolean(ColType): ...

class Enum(ColVal):
    def __init__(self, e: Type[enum.Enum]) -> None: ...