"""
HGI Beaver - Software Provisioning
Copyright (C) 2022 Michael Grace <mg38@sanger.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Generator, Type

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import MetaBase

DATABASE_URL: str = "mysql+mysqlconnector://beaver:beaverPass@localhost/beaver"

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Type[MetaBase] = declarative_base()


def create_db() -> None:
    """create the databse tables if needed"""
    Base.create_all(bind=engine)  # type: ignore


def get_db() -> Generator[sessionmaker, None, None]:
    """returns a database session"""
    database: sessionmaker = session()
    try:
        yield database
    finally:
        database.close()  # type: ignore
