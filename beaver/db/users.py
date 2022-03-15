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


class User(Base):
    """class representing a user"""
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)

    @staticmethod
    def get_or_make_user_id_for_user_name(username: str, database: Session) -> int:
        """get user id for the username given
            if they don't exist in the database - make them

        Args:
            - username: str - the username to search for/add if needed
            - database: Session - the database session

        Returns: int - the found or newly created user ID

        """

        user_id: int
        try:
            user_id = int(database.query(User).filter(
                User.user_name == username).one().user_id)
        except NoResultFound:
            new_user = User(user_name=username)
            database.add(new_user)
            database.commit()
            database.refresh(new_user)
            user_id = int(new_user.user_id)

        return user_id
