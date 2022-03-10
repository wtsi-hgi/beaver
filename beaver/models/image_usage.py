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

import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from beaver.models.groups import Group
from beaver.models.users import User
from beaver.models.images import Image


class ImageUsageBase(BaseModel):
    """base representation of an image usage dataset"""
    image_id: int
    user_id: int
    group_id: int


class ImageUsage(ImageUsageBase):
    """full representation of an image usage dataset"""
    image: Image
    user: User
    group: Group
    datetime: datetime.datetime

    class Config:
        """orm config"""
        orm_mode = True
