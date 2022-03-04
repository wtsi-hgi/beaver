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

from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from beaver.db.db import Base
from beaver.models.names import ImageNameElements


class ImageNameAdjective(Base):
    """class models adjectives for image names"""

    __tablename__ = "image_name_adjectives"
    adjective = Column(String, primary_key=True)


class ImageNameName(Base):
    """class models names for image names"""

    __tablename__ = "image_name_names"
    name = Column(String, primary_key=True)


def get_names(database: Session) -> ImageNameElements:
    """returns all the elements that could make up an image name"""
    return ImageNameElements(
        adjectives=[x.adjective for x in database.query(  # type: ignore
            ImageNameAdjective).all()],
        names=[x.name for x in database.query(  # type: ignore
            ImageNameName).all()]
    )


def create_names(database: Session, item: ImageNameElements) -> ImageNameElements:
    """adds elements to the lists of possible image name elements"""
    for adj in item.adjectives:
        db_adj_item = ImageNameAdjective(adjective=adj)  # type: ignore
        database.add(db_adj_item)  # type: ignore

    for name in item.names:
        db_name_item = ImageNameName(name=name)  # type: ignore
        database.add(db_name_item)  # type: ignore

    database.commit()
    return item
