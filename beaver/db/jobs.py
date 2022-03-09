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
from datetime import datetime, timedelta

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base
from beaver.db.images import Image
from beaver.models.jobs import JobStatus


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


def get_num_jobs_in_status(status: JobStatus, database: Session) -> int:
    """get number of jobs in the status `status`

    Args:
        status: JobStatus - the status to filter for

    """
    return database.query(Job).filter(  # type: ignore
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

    return database.query(Job).filter(  # type: ignore
        Job.status == status.value).filter(
            Job.endtime > datetime.now() - timedelta(hours=hours)  # type: ignore
    ).count()


def get_job(database: Session, job_id: str) -> Job:
    """return a particular job, identified by `job_id`

    Args:
        job_id: str - the ID of the job
            (note this is a string as it is a UUID)

    """
    return database.query(Job).filter(Job.job_id == job_id).one()  # type: ignore
