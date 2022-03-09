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

import enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class JobInfo(BaseModel):
    """represents basic information about all jobs"""
    jobs_queued: int
    jobs_building_definition: int
    jobs_pending_image_build: int
    jobs_building_image: int
    jobs_completed_last_24_hours: int
    jobs_failed_last_24_hours: int


class JobStatus(enum.Enum):
    """statuses a job can be in"""

    Queued = enum.auto()  # pylint: disable=invalid-name
    BuildingDefinition = enum.auto()  # pylint: disable=invalid-name
    DefinitionMade = enum.auto()  # pylint: disable=invalid-name
    BuildingImage = enum.auto()  # pylint: disable=invalid-name
    Succeeded = enum.auto()  # pylint: disable=invalid-name
    Failed = enum.auto()  # pylint: disable=invalid-name
