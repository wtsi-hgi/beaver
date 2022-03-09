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

from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.groups import Group
from beaver.db.users import User


class Image(Base):
    """class models a built image"""

    __tablename__ = "images"
    image_id = Column(Integer, primary_key=True)
    image_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))

    user: RelationshipProperty[User] = relationship("User")
    group: RelationshipProperty[Group] = relationship("Group")


class ImageContents(Base):
    """shows the contents of images"""

    __tablename__ = "image_contents"
    image_contents_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    package_id = Column(Integer, ForeignKey("packages.package_id"))


def get_images_for_user(database: Session, user_id: int) -> List[Image]:
    """gets images available for the specific user"""
    return database.query(Image).filter(Image.user_id == user_id).all()  # type: ignore
