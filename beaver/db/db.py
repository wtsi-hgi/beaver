"""
HGI Beaver - Software Provisioning
Copyright (C) 2022 Genome Research Limited

Author: Michael Grace <mg38@sanger.ac.uk>

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

engine = None  # pylint: disable=invalid-name
session = lambda: sessionmaker()  # pylint: disable=unnecessary-lambda


def create_connectors(database_url: str):
    """update the engine and session variables
    using `database_url`
    """

    global engine, session  # pylint: disable=global-statement, invalid-name

    if database_url.startswith("sqlite"):
        connect_args = {
            "check_same_thread": False
        }
    else:
        connect_args = {}

    engine = create_engine(database_url, connect_args=connect_args)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base: Type[MetaBase] = declarative_base()


def create_db() -> None:
    """create the databse tables if needed"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[sessionmaker, None, None]:
    """returns a database session"""
    database: sessionmaker = session()
    try:
        yield database
    finally:
        database.close()
