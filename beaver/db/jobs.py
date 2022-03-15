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
from datetime import datetime, timedelta
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.groups import Group
from beaver.db.images import Image, ImageContents
from beaver.db.users import User
import beaver.db.names
from beaver.models.jobs import BuildRequest, JobStatus


class Job(Base):
    """models a job"""

    __tablename__ = "jobs"
    job_id = Column(String, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.image_id"), nullable=False)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.Queued)
    detail = Column(String)
    starttime = Column(DateTime)
    endtime = Column(DateTime)

    image: RelationshipProperty[Image] = relationship("Image")


def get_num_jobs_in_status(status: JobStatus, database: Session) -> int:
    """get number of jobs in the status `status`

    Args:
        status: JobStatus - the status to filter for

    """
    return database.query(Job).filter(
        Job.status == status.value).count()


def get_num_jobs_in_status_last_n_hours(
    status: JobStatus,
    database: Session,
    hours: int = 24
) -> int:
    """get number of jobs in the status `status` with
        and endtime less than `hours` number of hours
        ago

    Args:
        status: JobStatus - the status to filter for
        hours: int (default 24) - the number of hours to filter with

    """

    return database.query(Job).filter(
        Job.status == status.value).filter(
            Job.endtime > datetime.now() - timedelta(hours=hours)
    ).count()


def get_job(database: Session, job_id: str) -> Job:
    """return a particular job, identified by `job_id`

    Args:
        job_id: str - the ID of the job
            (note this is a string as it is a UUID)

    """
    return database.query(Job).filter(Job.job_id == job_id).one()


def submit_job(database: Session, build: BuildRequest) -> Job:
    """create a new job and associated image and packages"""

    _request = build.dict()

    # First we're going to make the Image object
    # This requires turning the user and group names
    # provided into their respective IDs
    # We also need to generate an image name if it isn't
    # provided

    _user = _request["image"]["user_name"]
    _group = _request["image"]["group_name"]

    user_id: int = User.get_or_make_user_id_for_user_name(_user, database)
    group_id: int = Group.get_or_make_group_id_for_group_name(_group, database)

    image_name: str = beaver.db.names.generate_random_image_name(
        database, _user, _group) if not _request["image"].get("image_name") \
        else _request["image"]["image_name"]

    # IMPORTANT TODO: check the image name doesn't already exist
    # If it was auto generated, it won't, so if it does,
    # then we know we can just tell the user it already exists
    # and they need a new one

    # We can now add it to the DB
    new_image = Image(
        image_name=image_name,
        user_id=user_id,
        group_id=group_id
    )

    database.add(new_image)
    database.commit()
    database.refresh(new_image)
    image_id: int = int(new_image.image_id)

    # TODO: add new packages

    # Now we've got all our packages, we can add all the packages
    for package_id in _request["packages"]:
        _new_contents = ImageContents(
            image_id=image_id,
            package_id=package_id
        )
        database.add(_new_contents)
    database.commit()

    # Now we can actually create the job
    # Let's give it an ID
    _job_uuid: str = str(uuid.uuid4())
    while True:
        if database.query(Job).filter(Job.job_id == _job_uuid).count() == 0:
            break
        _job_uuid = str(uuid.uuid4())

    job: Job = Job(
        job_id=_job_uuid,
        image_id=image_id
    )

    database.add(job)
    database.commit()
    database.refresh(job)

    return job
