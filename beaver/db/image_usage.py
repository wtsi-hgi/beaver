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

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.groups import Group
from beaver.db.images import Image
from beaver.db.users import User


class ImageUsage(Base):
    """models image usage information"""

    __tablename__ = "image_usage"
    _dummy = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    datetime = Column(DateTime)

    user: RelationshipProperty[User] = relationship("User")
    group: RelationshipProperty[Group] = relationship("Group")
    image: RelationshipProperty[Image] = relationship("Image")
