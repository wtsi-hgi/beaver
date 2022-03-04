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
import beaver.db.names
from beaver.models.names import ImageNameElements


router = APIRouter(prefix="/names", tags=["names"])


@router.get("/", response_model=ImageNameElements)
async def get_names(database: Session = Depends(get_db)):
    """returns the possible elements for creating image names"""
    return beaver.db.names.get_names(database)


@router.post("/", response_model=ImageNameElements)
async def new_name(item: ImageNameElements, database: Session = Depends(get_db)):
    """adds to the lists of possible elements of image names"""
    return beaver.db.names.create_names(database, item)


@router.patch("/")
async def update_names():
    """updates the lists of possible image name elements"""
    return None
