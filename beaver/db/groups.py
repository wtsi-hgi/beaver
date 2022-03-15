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

from sqlalchemy import Column, String, Integer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from beaver.db.db import Base


class Group(Base):
    """class representing a group"""
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String)

    @staticmethod
    def get_or_make_group_id_for_group_name(group_name: str, database: Session) -> int:
        """get the group id for a given group name, or add
        them to the database if they don't exist

        Args:
            - group_name: str - the name of the group to search
                for or add if not in the database
            - database: Session - the database session to use

        Returns: int - the found or newly created group ID

        """

        group_id: int
        try:
            group_id = int(database.query(Group).filter(
                Group.group_name == group_name).one().group_id)
        except NoResultFound:
            new_group = Group(group_name=group_name)
            database.add(new_group)
            database.commit()
            database.refresh(new_group)
            group_id = int(new_group.group_id)

        return group_id
