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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from beaver.db.db import get_db
import beaver.db.jobs
from beaver.db.jobs import get_num_jobs_in_status, get_num_jobs_in_status_last_n_hours
from beaver.models.jobs import JobInfo, JobStatus, Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=JobInfo)
async def get_basic_job_info(database: Session = Depends(get_db)) -> JobInfo:
    """return some info about number of jobs in various states"""
    return JobInfo(
        jobs_queued=get_num_jobs_in_status(
            JobStatus.Queued, database),
        jobs_building_definition=get_num_jobs_in_status(
            JobStatus.BuildingDefinition, database),
        jobs_pending_image_build=get_num_jobs_in_status(
            JobStatus.DefinitionMade, database),
        jobs_building_image=get_num_jobs_in_status(
            JobStatus.BuildingImage, database),
        jobs_completed_last_24_hours=get_num_jobs_in_status_last_n_hours(
            JobStatus.Succeeded, database),
        jobs_failed_last_24_hours=get_num_jobs_in_status_last_n_hours(
            JobStatus.Failed, database)
    )


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str, database: Session = Depends(get_db)) -> beaver.db.jobs.Job:
    """return the job identified by `job_id`"""
    return beaver.db.jobs.get_job(database, job_id)
