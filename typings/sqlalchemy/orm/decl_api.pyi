"""
        DISCLAIMER

        These types are very much made to work with our use case.
        SQLalchemy is much more generic than this.
        Don't try to reuse these.

"""

from typing import Any
from sqlalchemy.sql.schema import MetaData


class DeclarativeMeta:
    metadata: MetaData

    def __init__(self, *_, **__: Any) -> None: ...