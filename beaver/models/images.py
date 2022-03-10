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

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from beaver.models.groups import Group
from beaver.models.users import User


class ImageBase(BaseModel):
    """base representation of an image"""
    image_name: str
    user_id: int
    group_id: int


class Image(ImageBase):
    """full representation of an image"""
    image_id: int
    user: User
    group: Group

    class Config:
        """orm config"""
        orm_mode = True
