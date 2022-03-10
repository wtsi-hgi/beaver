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

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from beaver.db.db import get_db
import beaver.db.images
from beaver.models.images import Image


router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{user_id}", response_model=List[Image])
async def get_images_for_user(
    user_id: int,
    database: Session = Depends(get_db)
) -> List[beaver.db.images.Image]:
    """returns images available for the specific user"""
    return beaver.db.images.get_images_for_user(database, user_id)
