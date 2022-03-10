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
import beaver.db.image_usage
from beaver.models.image_usage import ImageUsage, ImageUsageBase

router = APIRouter(prefix="/images/usage", tags=["image_usage"])


@router.get("/byuser/{user}", response_model=List[ImageUsage])
async def get_image_usage_by_user(
    user: int,
    database: Session = Depends(get_db)
) -> List[beaver.db.image_usage.ImageUsage]:
    """returns image usage by the user specified"""
    return beaver.db.image_usage.get_image_usage_for_user(database, user)


@router.get("/bygroup/{group}", response_model=List[ImageUsage])
async def get_image_usage_by_group(
    group: int,
    database: Session = Depends(get_db)
) -> List[beaver.db.image_usage.ImageUsage]:
    """returns image usage by the group specified"""
    return beaver.db.image_usage.get_image_usage_for_group(database, group)


@router.get("/byimage/{image}", response_model=List[ImageUsage])
async def get_image_usage_by_image(
    image: int,
    database: Session = Depends(get_db)
) -> List[beaver.db.image_usage.ImageUsage]:
    """returns image usage by the image specified"""
    return beaver.db.image_usage.get_image_usage_by_image(database, image)


@router.get("/bypackage/{package}", response_model=List[ImageUsage])
async def get_image_usage_by_package(
    package: int,
    database: Session = Depends(get_db)
) -> List[beaver.db.image_usage.ImageUsage]:
    """returns image usage by the package specified"""
    return beaver.db.image_usage.get_image_usage_by_package(database, package)


@router.post("/", response_model=ImageUsage)
async def record_image_usage(
    image_usage: ImageUsageBase,
    database: Session = Depends(get_db)
) -> beaver.db.image_usage.ImageUsage:
    """records that an image has been used"""
    return beaver.db.image_usage.record_image_usage(database, image_usage)
