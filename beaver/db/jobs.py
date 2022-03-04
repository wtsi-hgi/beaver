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
import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.images import Image


class JobStatus(enum.Enum):
    """statuses a job can be in"""

    Queued = enum.auto()  # pylint: disable=invalid-name
    BuildingDefinition = enum.auto()  # pylint: disable=invalid-name
    DefinitionMade = enum.auto()  # pylint: disable=invalid-name
    BuildingImage = enum.auto()  # pylint: disable=invalid-name
    Succeeded = enum.auto()  # pylint: disable=invalid-name
    Failed = enum.auto()  # pylint: disable=invalid-name


class Job(Base):
    """models a job"""

    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    status = Column(Enum(JobStatus))
    detail = Column(String)
    starttime = Column(DateTime)
    endtime = Column(DateTime)

    image: RelationshipProperty[Image] = relationship("Image")
