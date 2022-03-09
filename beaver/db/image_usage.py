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

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.groups import Group
from beaver.db.images import Image, ImageContents
from beaver.db.users import User


class ImageUsage(Base):
    """models image usage information"""

    __tablename__ = "image_usage"
    image_usage_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    datetime = Column(DateTime)

    user: RelationshipProperty[User] = relationship("User")
    group: RelationshipProperty[Group] = relationship("Group")
    image: RelationshipProperty[Image] = relationship("Image")


def get_image_usage_for_user(database: Session, user: int) -> List[ImageUsage]:
    """get image usage for the particular user"""
    return database.query(ImageUsage).filter(ImageUsage.user_id == user).all()  # type: ignore


def get_image_usage_for_group(database: Session, group: int) -> List[ImageUsage]:
    """get image usage for the group"""
    return database.query(ImageUsage).filter(ImageUsage.group_id == group).all()  # type: ignore


def get_image_usage_by_image(database: Session, image: int) -> List[ImageUsage]:
    """get image usage for the image"""
    return database.query(ImageUsage).filter(ImageUsage.image_id == image).all()  # type: ignore


def get_image_usage_by_package(database: Session, package: int) -> List[ImageUsage]:
    """get image usage based on a particular package"""
    return database.query(ImageUsage).filter(  # type: ignore
        ImageContents.package_id == package).all()  # type: ignore
