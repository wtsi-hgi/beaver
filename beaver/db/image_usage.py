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

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.groups import Group
from beaver.db.images import Image, ImageContents
from beaver.db.users import User
from beaver.models.image_usage import ImageUsageBase


class ImageUsage(Base):
    """models image usage information"""

    __tablename__ = "image_usage"
    image_usage_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.now())

    user: RelationshipProperty[User] = relationship("User")
    group: RelationshipProperty[Group] = relationship("Group")
    image: RelationshipProperty[Image] = relationship("Image")


def get_image_usage_for_user(database: Session, user: int) -> List[ImageUsage]:
    """get image usage for the particular user"""
    return database.query(ImageUsage).filter(ImageUsage.user_id == user).all()


def get_image_usage_for_group(database: Session, group: int) -> List[ImageUsage]:
    """get image usage for the group"""
    return database.query(ImageUsage).filter(ImageUsage.group_id == group).all()


def get_image_usage_by_image(database: Session, image: int) -> List[ImageUsage]:
    """get image usage for the image"""
    return database.query(ImageUsage).filter(ImageUsage.image_id == image).all()


def get_image_usage_by_package(database: Session, package: int) -> List[ImageUsage]:
    """get image usage based on a particular package"""
    images_for_package = database.query(ImageContents).filter(
        ImageContents.package_id == package
    ).with_entities(ImageContents.image_id).subquery()

    return database.query(ImageUsage).filter(
        ImageUsage.image_id.in_(images_for_package)).all()


def record_image_usage(database: Session, image_usage: ImageUsageBase) -> ImageUsage:
    """record usage of an image in the database"""

    db_image_usage = ImageUsage(**image_usage.dict())
    database.add(db_image_usage)
    database.commit()
    database.refresh(db_image_usage)

    return db_image_usage
