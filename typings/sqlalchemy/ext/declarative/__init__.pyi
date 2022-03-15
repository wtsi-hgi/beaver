"""
        DISCLAIMER

        These types are very much made to work with our use case.
        SQLalchemy is much more generic than this.
        Don't try to reuse these.

"""

from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import Type

def declarative_base() -> Type[DeclarativeMeta]:
    ...